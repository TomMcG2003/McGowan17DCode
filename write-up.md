# Phase 3 Write-up

Team: **TEAM TH4**

I submitted my DAW via AMS: **true**

* * *

1. Answer the following:

	a. What six conditions can cause a page fault on this Intel architecture?
        
        - The P flag is present. This means that in a page-directory or a page-table entry that holds the operand is not present in physical memory. In other words, the page that the process is looking for is not in our physical memory and is in swap space.
        - The process running does not have the privilege to access the page. It can also be that the process is in supervisor mode and tries to access data in user-mode space. Another reason could be if the process tries to access user-mode addresses that have certain protection keys.
        - Code that is running in user-mode attempts to wrtie to read-only pages or if code that is running in supervisor mode tries to write to read-only pages. 
        - An instruction fetch to a address that corresponds to a physical location that has execution privleges turned off, which is also true if in supervisor mode.
        - One or more of the reserved bits in the paging-structure are set to 1.
        - An enclave access violates one of the specified access-controll requirements. 


	b. Which of the six conditions might not indicate a program error?

    The first condition (P flag). This condition means that the requested page is not in virtual memory, but might be in swap space. When this flag is present, the OS will need to look into swap space on the disk and when the page is found, swap it into phsyical memory and give it back to the process.

    c. Assuming the page fault did not result from a program error, what would the operating system have to do to allow the program's continued execution?

    The OS would need to put the process into a wait/blocked state while it fetches the requested page from swap space on the disk and swap it into physical memory.

    d. Like most interrupts, this interrupt results in kernel code executing. According to Intel's documentation, what information will be available to the interrupt handing routine for page faults?

    The OS will have access to the Page-Fault Error Code which is a 32 bit message that holds all of the flag bits. It will look through this code bit-by-bit and be able to identify the type of error that was thrown and operate based off of the error.

1. What C data types did `src/threads/palloc.c` use to track free pages?  Why was that a good choice?

    `palloc.c` uses a struct called <pool> which uses a bitmap to keep track of the free pages. This is a good choice because assuming you can identify the number of pages (assuming you allocate them contigusously by process) the process holds. You can then use the bit indeces as the page identifiers. This is similar to how we used an array to track the PIDs in the previous phases.

1. You were asked to run `shell` within Pintos before you had made any changes to Pintos. The shell program should have crashed when you did this. Describe precisely why `shell` crashed, referencing the reading you did about [demand paging](https://en.wikipedia.org/wiki/Demand_paging).

    `shell` crashed because we did not implement any of the paging functions. Eventually, Pintos (and every OS) will have a protocol that will load the required pages for a program into physical memory. Pintos will use a lazy page loader meaning that it doesn't load a page into physical memory until it is requested. This also means that when it is initialized, there are no pages in physical memory. `shell` runs without its pages in physical memory and cannot retrieve them from the disk because there is no page loading function (yet) and throws a page-fault exception.

    In other words, `shell` can't find its pages in physical memory and the OS cannot retrieve them from the disk so it cannot execute. 

* * *
