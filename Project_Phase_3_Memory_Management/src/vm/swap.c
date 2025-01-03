#include "vm/swap.h"
#include <bitmap.h>
#include <debug.h>
#include <stdio.h>
#include "vm/frame.h"
#include "vm/page.h"
#include "threads/synch.h"
#include "threads/vaddr.h"
#include "devices/block.h"

typedef unsigned long elem_type;
size_t first_bit_in_sector;
struct bitmap
  {
    size_t bit_cnt;     /* Number of bits. */
    elem_type *bits;    /* Elements that represent bits. */
  };


/* The swap device. */
static struct block *swap_device;

/* Used swap frames. */
/* TODO (Phase 3): Implement data structure to track which frames
 * in swap space are in use. */
static struct bitmap *frames; 
/* Protects data structure above. */
static struct lock swap_lock;

#define PG_SIZE (1 << PGBITS)
#define BYTES_PER_SECTOR 512
// A sector is a row of block

/* Number of Sectors for an entire page */
#define SECTORS_PER_PAGE (PG_SIZE / BYTES_PER_SECTOR) // This is the number of sectors that a given page needs.
// If SECTORS_PER_PAGE <= block_size then we have enough space

/* Sets up swap. */
void
swap_init (void)
{
  swap_device = block_get_role (BLOCK_SWAP);

  if (swap_device == NULL)
    {
      printf ("no swap device--swap disabled\n");
    }
  else
    {
      /* TODO (Phase 3): Initialize swap-tracking data structure. */
      size_t bit_count = block_size(swap_device)/SECTORS_PER_PAGE;

      frames = bitmap_create(bit_count);
      bitmap_set_all(frames, false);
    }
  lock_init (&swap_lock);
}

/* Swaps in page P, which must have a locked frame
   (and be swapped out). */
void
swap_in (struct page *p)
{
  ASSERT (p->frame != NULL);
  ASSERT (lock_held_by_current_thread (&p->frame->lock));
  ASSERT (p->sector != (block_sector_t) -1);

  /* TODO (Phase 3): Read enough blocks to load page. */
  int i;
  for(i = 0; i < SECTORS_PER_PAGE; i++){
    block_read(swap_device, p->sector+i, p->frame->base+(i*BYTES_PER_SECTOR));
  }
  /* TODO (Phase 3): Mark swap frame as in use in tracking data structure. */
  // first_bit_in_sector = bitmap_scan_and_flip(frames, (size_t) 0, (size_t) SECTORS_PER_PAGE, false);
  lock_acquire(&swap_lock);
  bitmap_set(frames, (p->sector)/SECTORS_PER_PAGE, false);
  lock_release(&swap_lock);
  p->sector = (block_sector_t) -1;
}

/* Swaps out page P, which must have a locked frame. */
bool
swap_out (struct page *p)
{
  size_t slot = 0;

  ASSERT (p->frame != NULL);
  ASSERT (lock_held_by_current_thread (&p->frame->lock));

// Find some place that is true in the bitmap
  //size_t slot;
  //for (slot = 0; slot < bitmap_size(frames) && (&frames[slot] == true); slot++){}
  lock_acquire(&swap_lock);
  slot = bitmap_scan_and_flip(frames, 0, 1, false);
  lock_release(&swap_lock);
  /* Make sure we got a slot. */
  if (slot == BITMAP_ERROR)
    return false;
  // Writing from physical to disk
  // record the sector as the fist sector on in disk
  /* TODO (Phase 3): Assign a free swap frame to slot (instead of 0), and
   * mark that frame used in tracking data structure. */
  p->sector = slot*SECTORS_PER_PAGE;
  int i;
  for(i = 0; i < SECTORS_PER_PAGE; i++){
    block_write(swap_device, p->sector+i, p->frame->base+(i*BYTES_PER_SECTOR));
  }

  /* TODO (Phase 3): Write page across blocks on disk. */
 

  p->private = false;
  p->file = NULL;
  p->file_offset = 0;  // # of bytes needed - # of bytes allocated 
  p->file_bytes = 0;

  return true;
}
