* * *
# CS481: finalproject
### Cadet: Tom McGowan
### DAW: Assistance received (ChatGPT consulted re access controls)
### Early: 25
### Total Score: 236 / 250
* * *


Rubric Components:
* GrayFS Implementation (160): 152
    * mkdir (10): 10
    * rmdir (10): 10
    * readdir (10): 10
    * create (10): 10
    * truncate (10): 8
    * open (10): 10
    * read (10): 5
        * The final parameter to updateTimes determines whether the last status change time gets updated. Use it in chmod/chown-like calls.
    * write (10): 5
        * You need to be careful about how you handle requests to write a buffer that is too large
        * Return an error code rather than out.
    * unlink (10): 10
    * rename (10): 10
    * mknod (10): 10
    * symlink (10): 10
    * readlink (10): 10
    * chmod (10): 10
    * chown (10): 10
    * utimens(10): 9
        * Ignores time arguments
NOTE TO INSTRUCTOR: I only take off 1 point for failing to use the time arguments
        * utimens results: 2/3 tests passed
    * access (bonus): 5
        * In your read_write_checker, sometimes you set the return value, but you don't return at that point. In the end, you return 0.

* Code is readable (40): 38
    * Uses constants and not magic numbers(10): 10
    * Spacing is clean and consistent (10): 10
    * Code is understandable with appropriate comments/documentation (10): 8
    * Unused code has been removed and not just commented out (10): 10 (modulo access)

* Reflection (50): 46
    * Thoughtful responses to question about course (20): 16
    * Grayfs Function Implementation (30):
        * Provides a reasonable attempt (15):
        * Performs reasonable error checking (5):
        * Logic of implementation (5):
        * Correct implementation (5):

Passed 42 of 53 tests

* Test Details:
    * mount results: 2/2 tests passed
    * file system crashes: 0
    * mkdir results: 7/7 tests passed
    * rmdir results: 3/3 tests passed
    * readdir results: 3/3 tests passed
    * create results: 5/5 tests passed
    * unlink results: 3/3 tests passed
    * read results: 1/3 tests passed
        * read(foo.txt): --> test_read: [Errno 13] Permission denied
        * read(bye_link): --> test_read: [Errno 13] Permission denied
        * read(file-does-not-exist, ... ): PASS
    * write results: 0/5 tests passed
        * write(foo.txt, 'foo_file_content') --> test_write: [Errno 13] Permission denied
        * write(baz.txt, 'baz_baz_baz_baz_baz_') --> test_write2: [Errno 13] Permission denied
        * write(foo/bar/bye.txt, 'bye_file_content') --> test_write: [Errno 13] Permission denied
        * write(too_large.txt, 'len(buf)=4096, offset=0') --> test_error_write_too_big: [Errno 13] Permission denied
        * write(too_large.txt, 'len(buf)=9, offset=1022') --> test_error_write_too_big: [Errno 13] Permission denied
    * truncate results: 1/4 tests passed
        * truncate(foo.txt, 3) --> test_truncate: [Errno 13] Permission denied: '/data/CS481/faculty/maria.ebling/testfs/foo.txt'
        * truncate(foo.txt, 512) --> test_truncate: [Errno 13] Permission denied: '/data/CS481/faculty/maria.ebling/testfs/foo.txt'
        * truncate(foo.txt, 4097): FAIL
        * truncate(file-does-not-exist, ... ): PASS
    * rename results: 2/2 tests passed
    * chmod results: 2/2 tests passed
    * chown results: 3/3 tests passed
    * utimens results: 2/3 tests passed
        * utimens(foo.txt): PASS
        * utimens(foo.txt): FAIL
        * utimens(file-does-not-exist, ... ): PASS
    * symlink results: 2/2 tests passed
    * readlink results: 2/2 tests passed
    * mknod results: 2/2 tests passed
