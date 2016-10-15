# #
# # This file is placed under the public domain.
# #

import os
import sys
import imp
import traceback
import unittest
import optparse
import random
import subprocess
import time
import inspect

from . import support, testrunner

if sys.version_info[0] >= 3:
    MAXINT = sys.maxsize
else:
    MAXINT = sys.maxint

LINEDELIM = "-" * 70
HEAVYDELIM = "=" * 70

# Excludes
EXCLUDETAGS = ["interactive"]


def printerror():
    """Prints the last exception trace."""
    print(traceback.format_exc())


def include_tag(option, opt, value, parser, *args, **kwargs):
    try:
        if args:
            EXCLUDETAGS.remove(args[0])
        else:
            EXCLUDETAGS.remove(value)
    finally:
        pass


def exclude_tag(option, opt, value, parser, *args, **kwargs):
    if value not in EXCLUDETAGS:
        EXCLUDETAGS.append(value)


def list_tags(option, opt, value, parser, *args, **kwargs):
    alltags = []
    testsuites = []
    testdir, testfiles = gettestfiles(os.path.join
                                      (os.path.dirname(__file__), ".."))
    testloader = unittest.defaultTestLoader

    for test in testfiles:
        try:
            testmod = os.path.splitext(test)[0]
            fp, pathname, descr = imp.find_module(testmod, [testdir, ])
            package = imp.load_module(testmod, fp, pathname, descr)
            try:
                testsuites.append(loadtests_frompkg(package, testloader))
            except:
                printerror()
        except:
            pass
    for suite in testsuites:
        for test in suite:
            if hasattr(test, "__tags__"):
                tags = getattr(test, "__tags__")
                for tag in tags:
                    if tag not in alltags:
                        alltags.append(tag)
    print(alltags)
    sys.exit()


def create_options():
    """Create the accepatble options for the test runner."""
    optparser = optparse.OptionParser()
    optparser.add_option("-f", "--filename", type="string",
                         help="execute a single unit test file")
    optparser.add_option("-s", "--subprocess", action="store_true",
                         default=False,
                         help="run everything in an own subprocess "
                         "(default: use a single process)")
    optparser.add_option("-t", "--timeout", type="int", default=70,
                         help="Timout for subprocesses before being killed "
                         "(default: 70s per file)")
    optparser.add_option("-v", "--verbose", action="store_true", default=False,
                         help="be verbose and print anything instantly")
    optparser.add_option("-r", "--random", action="store_true", default=False,
                         help="randomize the order of tests")
    optparser.add_option("-S", "--seed", type="int",
                         help="seed the randomizer(useful to "
                         "recreate earlier randomized test cases)")
    optparser.add_option("-i", "--interactive", action="callback",
                         callback=include_tag,
                         callback_args=("interactive",),
                         help="also execute interactive tests")
    optparser.add_option("-e", "--exclude", action="callback",
                         callback=exclude_tag, type="string",
                         help="exclude test containing the tag")
    optparser.add_option("-l", "--listtags", action="callback",
                         callback=list_tags,
                         help="lists all available tags and exits")
    optparser.add_option("--logfile", type="string",
                         help="save output to log file")
    optkeys = ["filename",
               "subprocess",
               "timeout",
               "random",
               "seed",
               "verbose"
               ]
    return optparser, optkeys


def gettestfiles(testdir=None, randomizer=None):
    """Get all test files from the passed test directory. If none is
    passed, use the default sdl test directory.
    """
    if not testdir:
        testdir = os.path.dirname(__file__)
    if testdir not in sys.path:
        sys.path.append(testdir)

    names = os.listdir(testdir)
    testfiles = []
    for name in names:
        if name.endswith("_test" + os.extsep + "py"):
            testfiles.append(name)
    if randomizer:
        randomizer.shuffle(testfiles)
    else:
        testfiles.sort()
    return testdir, testfiles


def loadtests_frompkg(package, loader):
    for x in dir(package):
        val = package.__dict__[x]
        if hasattr(val, "setUp") and hasattr(val, "tearDown"):
            # might be a test.
            return loader.loadTestsFromTestCase(val)


def loadtests(package, test, testdir, writer, loader, options):
    """Loads a test."""
    suites = []
    try:
        testmod = os.path.splitext(test)[0]

        fp, pathname, descr = imp.find_module(testmod, [testdir, ])
        package = imp.load_module("%s.%s" % (package, testmod), fp, pathname,
                                  descr)
        if options.verbose:
            writer.writeline("Loading tests from [%s] ..." % testmod)
        else:
            writer.writesame("Loading tests from [%s] ..." % testmod)
        try:
            suites.append(loadtests_frompkg(package, loader))
        except:
            printerror()
    except:
        printerror()
    return suites


def prepare_results(results):
    testcount = 0
    errors = []
    failures = []
    skips = []
    ok = 0
    for res in results:
        testcount += res.testsRun
        ok += res.testsRun - len(res.errors) - len(res.failures) - \
            len(res.skipped)
        errors.extend(res.errors)
        skips.extend(res.skipped)
        failures.extend(res.failures)
    return testcount, errors, failures, skips, ok


def validate_args(options):
    if options.subprocess and options.filename:
        raise RuntimeError("-s cannot be used together with -f")


def run():
    optparser, optkeys = create_options()
    options, args = optparser.parse_args()
    validate_args(options)
    if options.logfile:
        openlog = open(options.logfile, 'wb')
        savedstd = sys.stderr, sys.stdout
        # copy stdout and stderr streams to log file
        sys.stderr = support.TeeOutput(sys.stderr, openlog)
        sys.stdout = support.TeeOutput(sys.stdout, openlog)
    writer = support.StreamOutput(sys.stdout)

    if options.verbose and not options.subprocess:
        writer.writeline(HEAVYDELIM)
        writer.writeline("-- Starting tests --")
        writer.writeline(HEAVYDELIM)

    randomizer = None
    if options.random:
        if options.seed is None:
            options.seed = random.randint(0, MAXINT)
        randomizer = random.Random(options.seed)
    loader = testrunner.TagTestLoader(EXCLUDETAGS, randomizer)

    testdir, testfiles = None, None
    if options.filename is not None:
        testdir = os.path.dirname(os.path.abspath(options.filename))
        testfiles = [os.path.basename(options.filename), ]
    else:
        testdir, testfiles = gettestfiles(os.path.join
                                          (os.path.dirname(__file__), ".."),
                                          randomizer=randomizer)

    if options.subprocess:
        overall = 0
        timeout = options.timeout
        gettime = time.time
        curmodule = "%s.%s" % (__package__, inspect.getmodulename(__file__))
        for test in testfiles:
            writer.write("Executing tests from [%s]... " % test)
            procargs = [sys.executable, "-m", curmodule]
            procargs += ["-f", os.path.join(testdir, test)]
            proc = subprocess.Popen(procargs, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            maxtime = gettime() + timeout
            retval = None
            while retval is None and gettime() < maxtime:
                retval = proc.poll()
            if retval is None:
                proc.kill()
                writer.writeline("execution timed out")
            elif retval != 0:
                writer.writeline("ERROR")
                writer.write(proc.stdout.read().decode("utf-8"))
                writer.writeline()
                overall = 1
            else:
                writer.writeline("OK")
                if options.verbose:
                    writer.write(proc.stdout.read().decode("utf-8"))
                    writer.writeline()
        return overall

    testsuites = []
    package = __package__.rsplit(".", 1)[0]
    for test in testfiles:
        testsuites.extend(loadtests(package, test, testdir, writer, loader,
                                    options))
    if not options.verbose:
        writer.writesame("Tests loaded")
    runner = testrunner.SimpleTestRunner(sys.stderr, options.verbose)

    results = []
    timetaken = 0

    if options.verbose:
        writer.writeline(HEAVYDELIM)
        writer.writeline("-- Executing tests --")
        writer.writeline(HEAVYDELIM)

    maxcount = 0
    for suite in testsuites:
        maxcount += suite.countTestCases()

    class writerunning:
        def __init__(self, maxcount, verbose):
            self.curcount = 0
            self.maxcount = maxcount
            self.verbose = verbose

        def __call__(self, test=None):
            self.curcount += 1
            if not self.verbose:
                if test:
                    writer.writesame("Running tests [ %d / %d ] [ %s ] ..." %
                                     (self.curcount, self.maxcount, test))
                else:
                    writer.writesame("Running tests [ %d / %d ] ..." %
                                     (self.curcount, self.maxcount))

    runwrite = writerunning(maxcount, options.verbose)

    for suite in testsuites:
        result = runner.run(suite, runwrite)
        timetaken += result.duration
        results.append(result)
    writer.writeline()
    testcount, errors, failures, skips, ok = prepare_results(results)

    writer.writeline(HEAVYDELIM)
    writer.writeline("-- Statistics --")
    writer.writeline(HEAVYDELIM)
    writer.writeline("Python:         %s" % sys.executable)
    writer.writeline("Options:")
    for key in optkeys:
        writer.writeline("                '%s' = '%s'" %
                         (key, getattr(options, key)))
    writer.writeline("                'excludetags' = '%s'" % EXCLUDETAGS)
    writer.writeline("Time taken:     %.3f seconds" % timetaken)
    writer.writeline("Tests executed: %d " % testcount)
    writer.writeline("Tests OK:       %d " % ok)
    writer.writeline("Tests SKIPPED:  %d " % len(skips))
    writer.writeline("Tests ERROR:    %d " % len(errors))
    writer.writeline("Tests FAILURE:  %d " % len(failures))

    if len(errors) > 0:
        writer.writeline("Errors:" + os.linesep)
        for err in errors:
            writer.writeline(LINEDELIM)
            writer.writeline("ERROR: %s" % err[0])
            writer.writeline(HEAVYDELIM)
            writer.writeline(err[1])
    if len(failures) > 0:
        writer.writeline("Failures:" + os.linesep)
        for fail in failures:
            writer.writeline(LINEDELIM)
            writer.writeline("FAILURE: %s" % fail[0])
            writer.writeline(HEAVYDELIM)
            writer.writeline(fail[1])
    if options.logfile:
        sys.stderr, sys.stdout = savedstd
        openlog.close()
    if len(errors) > 0 or len(failures) > 0:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(run())
