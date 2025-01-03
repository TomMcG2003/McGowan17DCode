/*
 * Long Gray Line File System
 * Copyright (C) 2022 Maria R. Ebling, Ph.D <maria.ebling@westpoint.edu>
 */

#ifndef _GFS_HELPER_H
#define _GFS_HELPER_H 1

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdbool.h>
#include "./grayfs.h"

/*
 * FileType - an enumeration of the different types of file objects.
 */
enum FileType {GrayDir, GrayFile, GrayLink, GrayDev};

/*
 * gray_fobj - a file object in Gray FS
 */
struct gray_fobj {
    enum FileType type;               // Type of the file object (dir, file, link, dev)
    char name[GRAY_NAME_SIZE];        // Name of the file object
    mode_t mode;                      // Mode and file-type indicator --> Permission bits!!!
    uid_t user_id;                    // User ID of the file object's owner --> Owner
    gid_t group_id;                   // Group ID of the file object's group --> Group
    time_t atime;                     // Time of last access
    time_t mtime;                     // Time of last modification
    time_t ctime;                     // Time of last status change -> update with CHMOD/CHGROUP
    char *extended_attr;              // Initialize dictionary of extended attributes
    char content[GRAY_MAX_FILESIZE];  // Content, if file object
    int length;                       // Length of the file
    int nlink;                        // Number of links
    struct gray_fobj *parent;         // Internal: Used for directory hierarchy
    struct gray_fobj *children;       // Internal: Used for directory hierarchy
    struct gray_fobj *sibling;        // Internal: Used for directory hierarchy
};

/**
 * children pointer holds the oldest child. All other children are interpretted
 * as sibilings of the oldest child. They all have the same parent pointer.
 * Files cannot have chilren, only directories can have children!!!
 */

char *gray_basename(char *path);
char *gray_dirname(char *path);

void get_permissions_h(struct gray_fobj *file, int mask, 
						int *array, int size);
void decode_flag(int flag, int *dump, int size);

int allows(int flag, int mode);
int read_write_checker(struct gray_fobj *file);
// Initialize a file object obj with the given type and name
void init_fobj(struct gray_fobj* obj, enum FileType type, char *name);

// Insert the child file object into the parent. Parent must be a GrayDir.
void gray_insert(struct gray_fobj *parent, struct gray_fobj *child);

// Remove the child file object
void gray_remove(struct gray_fobj *child);

// Fill the stat_buf with the stat information of the object
void gray_stat(struct gray_fobj *object, struct stat *stat_buf);

// Read length bytes of the file object, starting at offset
int gray_read(struct gray_fobj *file, char *buffer, int offset, int length);

// Write buffer into the file object, starting at offest
int gray_write(struct gray_fobj *file, int offset, char *buffer);

// Truncate the file object to the specified length
void gray_truncate(struct gray_fobj *file, int length);

// Update the accessed, modified, state change times of the object
void updateTimes(struct gray_fobj *object, bool accessed, bool modified, bool status);

// Return the file object specified by path starting at start
struct gray_fobj *gray_child(struct gray_fobj *start, char *path);

// Return the file object specified by path, traversing from root
struct gray_fobj *getFileObject(struct gray_fobj *root, char *path);

// Print out a directory listing, a file listing, or the contents of an object */
void printDirFull(struct gray_fobj *directory);
void printObject(struct gray_fobj *object);
void printObjectContent(struct gray_fobj *object);

#endif /* "./gfs-helper.h" included */
