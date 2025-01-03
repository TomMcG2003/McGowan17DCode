## Project Phase 3: Memory Management

*Assigned-team effort (100 pts)*

During the course of this phase, you will improve the memory management features of Pintos. First, you will modify Pintos' page fault handler so that it loads pages from a disk-based [swap space](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys.pdf). Next, you will complete Pintos' implmentation of swap space management. Finally, you will tune the page replacement strategy that Pintos uses to select which pages to evict.

You will implement swap space on top of a special disk partition that the Pintos' build process creates. Your code will use low-level disk reading routines to move data between main memory and this disk partition. Through this management, the kernel can give user space programs the illusion that the computer has more main memory than it actually does.

### Assumptions
* You have completed the `phase 2` assignment.
* You have accepted the `phase3` assignment in Github Classroom and entered your new team name from the Canvas assignment (e.g., SH-T1, SG-T5, etc).

### Artifacts

You must submit the following artifacts no later than 0600 on the due dates specifed in Canvas :

1. Project write up in the form of markdown file (writeup.md) via GitHub by Milestone 1 due date.
1. Source code, electronically submitted using GitHub by `Phase 3` due date.
1. e-Acknowledgement Statement should be submitted via Canvas on `Phase 3` due date, covering both milestones 1 and 2.
1. Team feedback due by 0600 on Milestone 2 due date using link in Canvas.

### Instructions

### Divergence from Previous Phases

The starting code for Phase 3 is different from that of the prior phases.  There are notable differences in how userspace processes are managed, but they are out of scope for this project.

### Introduction

:warning: **During this phase, build Pintos from the `src/vm` directory.** :warning:

Doing so will result in the build system building a version of Pintos that can support virtual-memory features such as swapping.

#### Page Faults

Open Intel's [System Programming Guide](http://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-system-programming-manual-325384.pdf). Read about the page-fault exception (pp. 6-40 through 6-42), an interrupt that the MMU invokes when programs interact with memory in a certain way.

:red_circle: **Before you continue, answer write-up question 1; put your response in writeup.md.**

#### Pages in Pintos

Execute Pintos so that it runs the command shell upon booting:

```
../utils/pintos --no-vga -- -q run 'shell'
```

You should see something like the following:

```
Executing 'shell':
Page fault at 0x8048323: not present error reading page in user context.
shell: dying due to interrupt 0x0e (#PF Page-Fault Exception).
Interrupt 0x0e (#PF Page-Fault Exception) at eip=0x8048323
cr2=08048323 error=00000004
eax=00000000 ebx=00000000 ecx=00000000 edx=00000000
esi=00000000 edi=00000000 esp=bfffffe4 ebp=00000000
cs=001b ds=0023 es=0023 ss=0023
shell: exit(-1)
Execution of 'shell' complete.
```

As it executed, the shell generated a page fault. The version of Pintos you are now running implements demand paging, but does not correctly handle the page fault exception.

:red_circle: Stop, read the Wikipedia description of [demand paging](https://en.wikipedia.org/wiki/Demand_paging), and **answer write-up questions 2 and 3, adding your response to writeup.md**.

### `page_fault` procedure: demand paging
Your next task is to fix Pintos so that `shell` can run.

After reading about demand paging, study the `page_in` function, also studying its companion function, `do_page_in`.  These can be found in `vm/page.c`.

Notice that `do_page_in` in handles three cases:

1. a page that exists in swap space
2. a page that corresponds to a file in the file system
3. a new page.

Review the `TODO` comments in `src/userprog/exception.c`'s `page_fault` procedure. Implement the procedure call that will attempt to find and load pages from swap space into main memory when a page access results in a page fault.

After correcting `src/userprog/exception.c`'s `page_fault` procedure, you should find that shell runs. You should further find that programs, such as `echo` and `cat`, also work. It seems Pintos' page-fault handler now supports demand paging enough to lazily load programs.

:red_circle: **This completes Milestone 1.**

### Swapping Pages to Disk When Out of Memory
From the Pintos **shell** prompt, run `matmult`. You should see output such as this:

```
Executing 'shell':
Shell starting...
pintos> matmult
matmult: exit(-1958281213)
shell: exit(-1)
Execution of 'shell' complete.
Timer: 334 ticks
Thread: 280 idle ticks, 30 kernel ticks, 25 user ticks
hdb1 (filesys): 129 reads, 0 writes
hdc1 (swap): 0 reads, 0 writes
Console: 856 characters output
Keyboard: 0 keys pressed
Exception: 2528 page faults
Powering off...
```

Note that `matmult` exited with a bad status code and caused the parent `shell` program to crash as well. The program `matmult` performs a number of multiplications using large matrices. In doing so, the program uses around 3 MB of main memory. When added to the size of the kernel, this surpasses the size of memory provided by QEMU; that is, it exceeds around 4 MB.

### Complete Pintos' swap implementation

Review the `TODO` comments in `src/vm/swap.c`. Here you will need to implement three things:


1. a data structure that tracks which swap frames are in use.

> :warning: Refer to how Pintos keeps track of pages in `src/threads/palloc.c` as a guide.

2. functionality that writes pages from main memory to swap space
3. functionality that reads pages from swap space into main memory

After this work is complete, you should find that `matmult` properly runs without running out of memory. Upon successfully running, matmult sets its exit code to part of the result of its multiplications, namely `133693952`.

### A new page-replacement strategy

Run Pintos so that only `matmult` executes:

```
../utils/pintos --no-vga -- -q run matmult
```

If you look at Pintos' boot output, you should see the following line:

```
Exception: 2527 page faults
```

It turns out that although Pintos' swap system works, it is not efficient. Pintos' choice of pages to evict results in an excess of page faults. This would, in turn, increase the amount of disk I/O necessary to run `matmult` until it exits. Modify the function `pick_me` which exists in `src/vm/frame.c` so that Pintos makes better choices about which pages to evict. A good solution will run `matmult` with fewer than 1500 page faults. (Do not increase the amount of main memory provided by QEMU to Pintos!)

### Useful Pintos interfaces

You will need to make use of the following Pintos interfaces during the course of completing this project:

1. A number of useful constants:

	```c
    // The number of bytes in a page.
    #define PG_SIZE (1 << PGBITS)

    // The number of bytes in a disk sector.
	#define BYTES_PER_SECTOR 512

    // The number of sectors needed to store an entire page.
	#define SECTORS_PER_PAGE (PG_SIZE / BYTES_PER_SECTOR)
	```

2. The block-device procedures which exist in `src/devices/block.c`.  When a block device is a physical disk, a block maps to a physical disk sector. The following procedures read and write from/to block (disk) devices. Such devices are divided into evenly-sized sectors (see the constants above). You will use these procedures to manipulate the system's swap space, so you should use the global swap device as the device parameter. (If interested, you can find the initialization statement for swap device in `swap.c`.)

	```c
	// Return the total number of sectors in a device.
	block_sector_t block_size (struct block *device);

	// Read given sector number from device and place it in memory
	// at addr:
	void block_read (struct block *device, block_sector_t sector, void *addr);

	// Write one sector's worth of data, from memory beginning at addr,
	// to device at given sector number.
	void block_write (struct block *device, block_sector_t sector, const void *addr);
	```

3. A number of page-management-related procedures which exist in `src/vm/page.c`:

	```c
	// Return true if page's accessed bit is set.
	bool page_accessed_recently (struct page *p);

	// Attempt to load page which would contain fault addr from swap;
	// return true on success.
	bool page_in (void *fault_addr)
	```

4. The locking procedures which exist in `src/threads/synch.c`:

	```c
	void lock_init(struct lock *lock)  // Initialize a lock.
	void lock_acquire(struct lock *lock)  // Wait on a lock.
	void lock_release(struct lock *lock)  // Release a lock.
	```

    You ought to use locking whenever you manipulate an Operating System (OS) object that is available to more than one other objects (for example, a `struct file` object).

### Testing

A perfect solution with pass all of the tests that execute when you run `make clean all check` from within `src/vm/`. In addition, `matmult` should run until it exits with a status code of `133693952`. Finally, the execution of `matmult` should generate no more than 1,500 page faults.

### Write up

Answer the following questions:

1. Open Intel's System Programming Guide, which is available [here](http://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-system-programming-manual-325384.pdf). Read about the page-fault exception (pp 6-40 through 6-42), an interrupt that the MMU invokes when programs interact with memory in a certain way. Answer the following:

	* What six conditions can cause a page fault on this Intel architecture?
	* Which of the six conditions might not indicate a program error?
	* Assuming the page fault did not result from a program error, what would the operating system have to do to allow the program's continued execution?
	* Like most interrupts, this interrupt results in kernel code executing. According to Intel's documentation, what information will be available to the interrupt handing routine for page faults?
1. You were asked to run `shell` within Pintos before you had made any changes to Pintos. The shell program should have crashed when you did this. Describe precisely why `shell` crashed, referencing the reading you did about [demand paging](https://en.wikipedia.org/wiki/Demand_paging).
1. What C data types did `src/threads/palloc.c` use to track free pages?  Why was that a good choice?


### Grading

While the following will guide the grading of this project phase, your instructor reserves the right to deviate from this plan:

| Component  | Points |
| --- | --- |
|Correct implementation of the page fault method  | 10 |
|Correct implementation of the swap init method  | 10 |
|Correct implementation of the swap in method  | 10 |
|Correct implementation of the swap out method  | 10 |
|Maintain set of free swap frames  | 10 |
|Implement disk-based swap space  | 10 |
|Improve number of page faults in matmult to fewer than 1500  | 10 |
|Code is well-designed, clean, and descriptive  | 10  |
|Write up is complete and correct  | 20  |
|**Total** | **100** |
