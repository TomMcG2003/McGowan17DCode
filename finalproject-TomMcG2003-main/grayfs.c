/*
 * Long Gray Line File System
 * Copyright (C) 2022, 2023 Maria R. Ebling, Ph.D <maria.ebling@westpoint.edu>
 * Copyright (C) 2023 Thomas M. McGowan <thomas.mcgowan@westpoint.edu>
 */

#define FUSE_USE_VERSION 31

#include <fuse.h>
#include <libgen.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <utime.h>
#include <errno.h>
#include <fcntl.h>
#include <stddef.h>
#include <assert.h>
#include "./grayfs.h"
#include "./gfs-helper.h"
#include "./pathnames.h"
#include "./utils.h"

#define FALSE 0
#define TRUE 1
#define MAX_LINK_COUNT 128

/*
 * Define the root of our file system.
 */
struct gray_fobj root;
int access_counter = 0;
static int grayfs_access(const char* path, int mask);
/*
 * Command line options
 *
 * Note: We can't set default values for the char* fields here because
 * fuse_opt_parse would attempt to free() them when the user specifies
 * different values on the command line.
 */
static struct options {
	const char *filename;
	const char *contents;
	int show_help;
} options;

#define OPTION(t, p)                           \
    { t, offsetof(struct options, p), 1 }

static const struct fuse_opt option_spec[] = {
	OPTION("--name=%s", filename),
	OPTION("--contents=%s", contents),
	OPTION("-h", show_help),
	OPTION("--help", show_help),
	FUSE_OPT_END
};

/*
 * grayfs_init -- Initializes GrayFS
 */
static void *grayfs_init(struct fuse_conn_info *conn, struct fuse_config *cfg)
{
	// cfg->kernel_cache = 1;  // Maybe auto cache?
	cfg->auto_cache = 1;
	init_fobj(&root, GrayDir, "/");
	printf("Grayfs Up and Running!\n");
	return NULL;
}

/*
 * grayfs_getattr - Returns file attributes
 *
 * The stat structure is defined in detail in the stat(2) manual page.
 * For the specified pathname, this function should fill in the elements
 * of the stat structure. If a field is meaningless in the filesystem you
 * are building (e.g., st_ino), then it should be set to 0 or given a
 * "reasonable" value. This function is absolutely required for your file
 * system to run. It is called very, very frequently!
 *
 * Returns:
 *           0, if successful
 *     -ENOENT, if file object for path does not exist
 *
 * Note: We use a simplified getattr. See comments in TODO.
 */
static int grayfs_getattr(const char *path, struct stat *stbuf,
                          struct fuse_file_info *fi)
{
	// TODO (Phase 5)
	// NOTE: Complete and tested
	// Find the gray_fobj associated with path using gray_child helper function
	// Fill in stbuf with its stat information using gray_stat helper function

	int retValue = -ENOENT;
	char pathcpy [GRAY_MAX_PATHLENGTH];
	strncpy(pathcpy, path, GRAY_MAX_PATHLENGTH);
    struct gray_fobj *file = gray_child(&root, pathcpy);
	if (NULL != file){	
		memset(stbuf, 0, sizeof(struct stat));
    	gray_stat(file, stbuf);
		retValue = 0;	
	}

	return retValue;
}

/*
 * grayfs_access - Checks whether the calling process can access the path.
 */
static int grayfs_access(const char* path, int mask) {
	// Phase 5: This function is optional.
	
	/*int perm = file->mode & 0777;
	uid_t uid = file->user_id;
	gid_t gid = file->group_id;
	uid_t current_uid = getuid();
	gid_t current_gid = getgid();
	
	int temp [7];
	decode_flag(fi->flags, temp, 7);

	int flag;
	int this_perm;
	if (uid == current_uid){
		this_perm = (perm >> 6) & 7;
		flag = 2;
	} else if (gid == current_gid){
		this_perm = (perm >> 3) & 7;
		flag = 3;
	} else{
		this_perm = perm & 7;
		flag = 4;
	}
	*/
	
	return 0;
	

}

/***********************
 *****             *****
 ***** DIRECTORIES *****
 *****             *****
 ***********************/

/* grayfs_mkdir - Create a directory of the given name with the specified mode
 *
 * See the mkdir(2) man page for details
 * This function is required for any reasonable read-write file system
 */
// COMPLETE AND TESTED
int grayfs_mkdir(const char *path, mode_t mode) {
	// TODO (Phase 5)
	int returnValue = -ENOENT;
	char path_copy[GRAY_MAX_PATHLENGTH];
	char parent_path [GRAY_MAX_PATHLENGTH];
	char path_copy2 [GRAY_MAX_PATHLENGTH];
	strncpy(path_copy, path, GRAY_MAX_PATHLENGTH);
	strncpy(parent_path, path, GRAY_MAX_PATHLENGTH);
	strncpy(path_copy2, path, GRAY_MAX_PATHLENGTH);
	// We make some copies of the path
	if (path_copy == NULL || parent_path == NULL || path_copy2 == NULL){
		return returnValue;
	}
	char *name = gray_basename(path_copy);
	char *parent = gray_dirname(parent_path);
	// We grab the name of the file and the parent directory
	if (name == NULL){
		return -EINVAL;
	}
	else if (parent == NULL){
		return -ENOENT;
	}
	// Make sure that the parent exists and that the new dir doesn't already exist
	struct gray_fobj *doesItExist = getFileObject(&root, path_copy2);
	if (doesItExist != NULL){
		return -EEXIST;
	}
	//int perm =  access(parent, 2);
	//if (perm < 0){
	//	return -perm;
	//}
	struct gray_fobj *parentObj = getFileObject(&root, parent);
	if (parentObj == NULL && parentObj->type == GrayDir){
		return -ENOTDIR;
	}
	

	struct gray_fobj *newDir = malloc(sizeof(struct gray_fobj)); 
	if (newDir == NULL){
		return -ENOMEM;  // Change this
	}
	init_fobj(newDir, GrayDir, name);
	// We initialize the fobj
	gray_insert(parentObj, newDir);
	returnValue = 0;
	return returnValue;
}

/* grayfs_rmdir - Remove the directory of the given name
 *
 * See the rmdir(2) man page for details
 * This function is required for any reasonable read-write file system.
 * It should succeed ONLY if the directory is empty except for "." & "..".
 */
// COMPLETE AND TESTED
static int grayfs_rmdir(const char *path) {
	// TODO (Phase 5)
	// replace itself with its sibling
	int returnValue = -ENOENT;
	char path_copy [GRAY_MAX_PATHLENGTH];
	char path_copy2 [GRAY_MAX_PATHLENGTH];
	char path_copy3 [GRAY_MAX_PATHLENGTH];
	strncpy(path_copy, path, GRAY_MAX_PATHLENGTH);
	strncpy(path_copy2, path, GRAY_MAX_PATHLENGTH);
	strncpy(path_copy3, path, GRAY_MAX_PATHLENGTH);

	if (path_copy == NULL || path_copy2 == NULL || path_copy3 == NULL){
		return returnValue;
	}
	char *parent_path = gray_dirname(path_copy2);
	char *base = gray_basename(path_copy3);
	if (base == NULL || base == (char *) '.'){
		return -EINVAL;
	}
	struct gray_fobj *parent = getFileObject(&root, parent_path);
	struct gray_fobj *file = getFileObject(&root, path_copy);
	if (file == NULL || parent == NULL){
		return -ENOMEM;
	}
	if (file->children != NULL){
		return -ENOTEMPTY;
	}
	gray_remove(file);
	returnValue = 0;
	return returnValue;
}

/*
 * grayfs_readdir - Return one or more directory entries (fuse.Direntry)
 * This is one of the most complex FUSE functions.
 * This function is related to the readdir(2) and getdents(2) system
 * calls, as well as the readdir(3) library function.
 * This function is required for essentially any file system because
 * it is needed to make things like "ls" function.
 *
 * FUSE provides a "filler" function that helps you put things into the
 * buffer. Here's the declaration:
 *     int filler(void *buf, char *component, NULL, 0, 0)
 * You should always provide NULL, 0, 0 as the final three arguments.
 * Don't forget that YOU have to put . and .. into the buffer if the
 * object is a directory.
 */
// COMEPLTE AND TESTED
static int grayfs_readdir(const char *path, void *buf, fuse_fill_dir_t filler,
                          off_t offset, struct fuse_file_info *fi,
                          enum fuse_readdir_flags flags)
{
	// TODO (Phase 5)
	// Ignore the 'flags' parameter
	// Always send a zero to the filler function's offset
	int returnValue = -ENOENT;
	char pathcpy [GRAY_MAX_PATHLENGTH];
	strncpy(pathcpy, path, GRAY_MAX_PATHLENGTH);
	if (pathcpy == NULL){
		return -EBADFD;
	}
	struct gray_fobj *file = gray_child(&root, pathcpy);
	if (file != NULL){
		if (file->type == GrayDir){
			// add '.', '..'
			filler(buf, ".", NULL, 0, 0);
			filler(buf, "..", NULL, 0, 0);
			struct gray_fobj *child = file->children;
			// We now have the oldest child of the directory
			while(child != NULL){
				filler(buf, child->name, NULL, 0, 0);
				child = child->sibling;
			}
			returnValue = 0;
		}
		else{ // Not a directory
			filler(buf, file->name, NULL, 0, 0);
			returnValue = 0;
		} 
	}

	return returnValue;
}


/*************************
 *****               *****
 ***** REGULAR FILES *****
 *****               *****
 *************************/

/*
 * grayfs_create - Creates a file object named path with the given mode
 * See the creat(2) man page for details.
 */
// COMPLETE AND TESTED
static int grayfs_create(const char *path, mode_t mode, struct fuse_file_info *fi) {
	// TODO (Phase 5)
	int returnValue = -ENOENT;
	char pathCpy1 [GRAY_MAX_PATHLENGTH];
	char pathCpy2 [GRAY_MAX_PATHLENGTH];
	char pathCpy3 [GRAY_MAX_PATHLENGTH];
	strncpy(pathCpy1, path, GRAY_MAX_PATHLENGTH);
	strncpy(pathCpy2, path, GRAY_MAX_PATHLENGTH);
	strncpy(pathCpy3, path, GRAY_MAX_PATHLENGTH);
	// The functions we call on these later are destructive so we do not need to deallocate
	if (pathCpy1 == NULL || pathCpy2 == NULL || pathCpy3 == NULL){
		return returnValue;
	} 
	// We have now saved the parent directory and the file name from the given path.
	char *directory = gray_dirname(pathCpy1);  // Maybe I check that if this is null, the directory is "."
	char *fileName = gray_basename(pathCpy2);
	if (fileName == NULL){
		return -EBADFD;
	}

	if (directory == NULL){
		return -EBADFD;
	}
	struct gray_fobj *doesItExist = getFileObject(&root, pathCpy3);
	if (doesItExist != NULL){
		return -EEXIST;
	}
	// We now have the parent directory of the file and the file name
	struct gray_fobj *parentDir = getFileObject(&root, directory);
	if (parentDir == NULL){
		return -ENOTDIR;
	}
	if (parentDir->type == GrayLink){
		return -ELOOP;
	}
	else if (parentDir->type != GrayDir){
		return -ENOTDIR;
	}
	struct gray_fobj *newFile = malloc(sizeof(struct gray_fobj)); 
	init_fobj(newFile, GrayFile,  fileName);	

	if (newFile == NULL){
		return -ENOMEM;
	}
	
	newFile->mode = S_IFREG | mode;

	// We now have the parent directory as an fobj and we have created the new file
	gray_insert(parentDir, newFile);
	// Lets insert the new file into the directory
	updateTimes(newFile, TRUE, TRUE, TRUE);	
	returnValue = 0;

	return returnValue;
}

/*
 * grayfs_truncate - Truncates the file object named path to the specified size
 * See the truncate(2) man page for details.
 */
// WORKS AS TESTED
static int grayfs_truncate(const char *path, off_t size,
                           struct fuse_file_info *fi)
{
	// TODO (Phase 5)
	int returnValue = -1;
	char path_copy [GRAY_MAX_PATHLENGTH];
	strncpy(path_copy, path, GRAY_MAX_PATHLENGTH);

	if (path_copy == NULL){
		return -EBADFD;
	}

	struct gray_fobj *file = getFileObject(&root, path_copy);
	if (file == NULL){
		return -ENOENT;
	}
	if (file->type == GrayDir){
		return -EISDIR;
	}

	int out = read_write_checker(file);
	if (out != 0){
		return out;
	}	

	 char buf [(int) size];
	 gray_read(file, buf, 0, (int) size);
	 // strncpy handles the truncation for us, we just need to write data into the contents.
	 if (buf != NULL){
		memset(file->content, '\0', GRAY_MAX_FILESIZE);
		gray_write(file, 0, buf);
		returnValue = 0;
		updateTimes(file, TRUE, TRUE, FALSE);
	 }
	return returnValue;
}

/*
 * grayfs_open - Opens the file object named path
 * See open(2) man page for details.
 */
// COMPLETE AND TESTED
static int grayfs_open(const char *path, struct fuse_file_info *fi) {
	// TODO (Phase 5) --> Implement flag checking
	/*
	 * Note: A real file system would check that the open flags in
	 * the system call request are permitted based on the mode of
	 * the file. Our simple file system will omit this check, though
	 * there might be bonus points available to you if you do
	 * implement this feature.
	 */
	// Return whether or not the file exists
	int returnValue = -ENOENT;
	char path_copy [GRAY_MAX_PATHLENGTH];
	strncpy(path_copy, path, GRAY_MAX_PATHLENGTH);
	if (path_copy == NULL){
		return -EBADF;
		// I picked this error number because it is used to denot a bad fd. 
		// We are using the path as the fd in this implementatio so I saw it
		// as fitting to use that error number.
	}

	struct gray_fobj *file = getFileObject(&root, path_copy);

	if (file == NULL){
		return -ENOENT;
	}

	// 0 == read
	// 2 == write
	
	int perm = file->mode & 0777;
	uid_t uid = file->user_id;
	gid_t gid = file->group_id;
	uid_t current_uid = getuid();
	gid_t current_gid = getgid();
	
	int temp [7];
	decode_flag(fi->flags, temp, 7);

	int flag;
	int this_perm;
	if (uid == current_uid){
		this_perm = (perm >> 6) & 7;
		flag = 2;
	} else if (gid == current_gid){
		this_perm = (perm >> 3) & 7;
		flag = 3;
	} else{
		this_perm = perm & 7;
		flag = 4;
	}
	
	returnValue = allows(temp[flag], this_perm) - 1;
	return returnValue;

}

/*
 * grayfs_read: Reads from a file
 * See read(2) man page for details.
 */
// NOTE: COMPLETE AND TESTED
static int grayfs_read(const char *path, char *buf, size_t size, off_t offset,
                       struct fuse_file_info *fi)
{
	// TODO (Phase 5)
	int returnValue = -1;
	char pathcpy [GRAY_MAX_PATHLENGTH];
	strncpy(pathcpy, path, GRAY_MAX_PATHLENGTH);

	if (pathcpy == NULL){
		return -EBADF;
	}

	struct gray_fobj *file = getFileObject(&root, pathcpy);
	
	if (file == NULL){
		return -EBADF;
	}
	
	if (file->type == GrayDir){
		return -EISDIR;
	}

	int out = read_write_checker(file);
	if (out != 0){
		return out;
	}
	int off = (int) offset;
	int read_size = (int) size;
	int chars = gray_read(file, buf, off, read_size);  
	updateTimes(file, TRUE, FALSE, FALSE); // IDK what to do with this last flag. Need to ask in AI

	returnValue = chars;
	return returnValue;
}

/*
 * grayfs_write: Writes to the file named path size bytes from the buf buffer
 * See write(2) man page for details.
 */
// COMPLETE AND TESTED
static int grayfs_write(const char *path, const char *buf, size_t size,
                        off_t offset, struct fuse_file_info *fi) {
	// TODO (Phase 5)
	int returnValue = -1;
	char pathcpy [GRAY_MAX_PATHLENGTH];
	strncpy(pathcpy, path, GRAY_MAX_PATHLENGTH);

	if (pathcpy == NULL){
		return -EBADFD;
	}

	struct gray_fobj *file = getFileObject(&root, pathcpy);

	if (file == NULL){
		return -EBADFD;
	}
	if (file->type == GrayDir){
		return -EISDIR;
	}
	
	int out = read_write_checker(file);
	if (out != 0){
		printf("You cannot wirte, buddy\n");
		return out;
	}

	int off = (int) offset;
	// Write the contents of the file into the buffer
	char protectedBuffer[GRAY_MAX_FILESIZE];
	strncpy(protectedBuffer, buf, (int) size);
	char realBuffer[(int)size];
	int i;
	for(i=0; i<(int) size; i++){
		realBuffer[i] = protectedBuffer[i];
	}
	returnValue = gray_write(file, off, realBuffer);
	updateTimes(file, TRUE, TRUE, FALSE); 
	return returnValue;
	// 16 is me trying to execute
	// 17 is the read request that is called when I try to execute
	// the "write successful" is me echoing into the file. No access check!
	// When I call "cat", There is no access check.
}

/*
 * grayfs_unlink - Removes the file object named path
 * See unlink(2) man page for details
 */ 
// COMPELTE AND TESTED
static int grayfs_unlink(const char *path) {
	// TODO (Phase 5)
	int returnValue = -ENOTSUP;
	char path_copy [GRAY_MAX_PATHLENGTH];
	char path_copy2 [GRAY_MAX_PATHLENGTH];
	strncpy(path_copy, path, GRAY_MAX_PATHLENGTH);
	strncpy(path_copy2, path, GRAY_MAX_PATHLENGTH);

	if (path_copy == NULL || path_copy2 == NULL){
		return -EBADFD;
	}
	char *parent_path = gray_dirname(path_copy2);
	struct gray_fobj *parent = getFileObject(&root, parent_path);
	struct gray_fobj *file = getFileObject(&root, path_copy);
	if (file == NULL || parent == NULL){
		return -ENOENT;
	}
	if (parent->type != GrayDir){
		return -ENOTDIR;
	}
	if (file->type == GrayDir){
		return -EPERM;
	}

	// Do we need to make sure that there are no links open?
	gray_remove(file);
	returnValue = 0;
	return returnValue;
}

/*
 * grayfs_rename - Renames a file within a single directory.
 * See the rename(2) man page for details.
 *
 * Note:
 * The rename(2) command is quite complex. This implementation supports only
 * the special case where from and to paths have the same parent. If that
 * condition does not hold, just return -ENOTSUP.
 */

// COMPLETE AND TESTED
static int grayfs_rename(const char *from, const char *to, unsigned int flags) {
	//  From and to are both paths!
	// TODO (Phase 5)
	int returnValue = -ENOTSUP;
	char from_copy [GRAY_MAX_PATHLENGTH];
	char to_copy [GRAY_MAX_PATHLENGTH];

	strncpy(from_copy, from, GRAY_MAX_PATHLENGTH);
	strncpy(to_copy, to, GRAY_MAX_PATHLENGTH);

	// Checks to make sure we correctly copied in the paths
	if (from_copy == NULL || to_copy == NULL){
		return -EBADFD;
	}

	// Grabs the files
	struct gray_fobj *old_file = getFileObject(&root, from_copy);
	// Checks to make sure we actually hae the file names.
	if (old_file == NULL){ 
		return -ENOENT;
	}

	char *newName = gray_basename(to_copy);
	if (newName == NULL){
		return -EINVAL;
	}

	// Ensures the condition of siblinghood is met
	strncpy(old_file->name, newName, GRAY_NAME_SIZE);
	updateTimes(old_file, TRUE, TRUE, FALSE);
	returnValue = 0;

	return returnValue;
}

/*********************************
 *****                       *****
 ***** SPECIAL FILES & LINKS *****
 *****                       *****
 *********************************/


/*
 * grayfs_mknod - Create a special (device) file, FIFO, or socket
 * See the mknod(2) man page for details
 * Ignore the dev number.
 */
// Kinda works
static int grayfs_mknod(const char *path, mode_t mode, dev_t rdev) {
	// TODO (Phase 5)
	int returnValue = -ENOTSUP;
	char path_copy [GRAY_MAX_PATHLENGTH];
	char path_copy2 [GRAY_MAX_PATHLENGTH];
	strncpy(path_copy, path, GRAY_MAX_PATHLENGTH);
	strncpy(path_copy2, path, GRAY_MAX_PATHLENGTH);
	if (path_copy == NULL || path_copy2 == NULL){
		return returnValue;
	}
	struct gray_fobj *doesItExist = getFileObject(&root, path_copy);
	if (doesItExist != NULL){
		return -EEXIST;
	}
	char *parent_path = gray_dirname(path_copy);
	char *devName = gray_basename(path_copy2);
	if (devName == NULL){
		return -ENOTDIR;
	}
	struct gray_fobj *parent = getFileObject(&root, parent_path);
	if (parent == NULL){
		return -ENOTDIR;
	}
	struct gray_fobj *newFile = malloc(sizeof(struct gray_fobj));
	
	init_fobj(newFile, GrayDev, devName);
	newFile-> mode = S_IFIFO | mode;
	
	updateTimes(newFile, TRUE, TRUE, TRUE);
	returnValue = 0;
	gray_insert(parent, newFile);
	return returnValue;
}
/*
 * grayfs_link - Create a link (also known as a hard link) to an existing file.
 *
 * Hard links are NOT supported by grayfs.
 * Implementation of hard links is non-trivial and not required for Phase 5.
 */
static int grayfs_link(const char *from, const char *to) {
	// NOT REQUIRED
	printf("grayfs_link: from:%s to:%s\n", from, to);
	return -ENOTSUP;
}

/*
 * grayfs_symlink - Create a symbolic link (also known as a symlink)
 * See the symlink(2) man page for details.
 */
// COMPLETE AND TESTED
static int grayfs_symlink(const char *from, const char *to) {
	// TODO (Phase 5)
	// FROM is the target
	// TO is the link name
	int returnValue = -ENOTSUP;

	char from_copy [GRAY_MAX_PATHLENGTH];
	char to_copy [GRAY_MAX_PATHLENGTH];
	char to_copy2 [GRAY_MAX_PATHLENGTH];

	strncpy(from_copy, from, GRAY_MAX_PATHLENGTH);
	strncpy(to_copy, to, GRAY_MAX_PATHLENGTH);
	strncpy(to_copy2, to, GRAY_MAX_PATHLENGTH);
	
	if (to_copy == NULL || to_copy2 == NULL || from_copy == NULL){
		return -ENOENT;
	}
	
	char *parent_dir = gray_dirname(to_copy);
	struct gray_fobj *parentObj = getFileObject(&root, parent_dir);

	if (parentObj == NULL){
		return -ENOENT;
	}

	char *link_name = gray_basename(to_copy2);
	struct gray_fobj *child = parentObj->children;  // This grabs the child of the obj
	// This while loop will check to make sure that it doesn't already exist
	while (child != NULL){
		if (link_name == child->name && GrayLink == child->type){
			// This means that they are the same file
			return -EEXIST;
		} else{
			child = child->sibling;
		}
	}

	struct gray_fobj *new_symlink = malloc(sizeof(struct gray_fobj));  // This is the new symlink
	init_fobj(new_symlink, GrayLink, link_name);
	if (new_symlink == NULL){
		return -ENOMEM;
	}
	gray_write(new_symlink, 0, from_copy);
	strncpy(new_symlink->content, from_copy, GRAY_MAX_FILESIZE);
	gray_insert(parentObj, new_symlink);
	updateTimes(new_symlink, TRUE, TRUE, TRUE);
	returnValue = 0;

	return returnValue;
}

/*
 * grayfs_readlink - Return the target of a symbolic link
 * See the readlink(2) man page for details.
 */
// COMPLETE AND TESTED
static int grayfs_readlink(const char *path, char *buf, size_t size) {
	// TODO (Phase 5)
	int returnValue = -1;
	char path_copy [GRAY_MAX_PATHLENGTH];
	
	strncpy(path_copy, path, GRAY_MAX_PATHLENGTH);
	if (path_copy == NULL || buf == NULL){ 
		return -EINVAL;
	}

	struct gray_fobj *symlink = getFileObject(&root, path_copy);
	if (symlink == NULL){
		return -ENOENT;
	}
	if (symlink->type != GrayLink){
		return -ENOENT;
	}
	int user_size = size;
	if (user_size < 0){
		return -EINVAL;
	}

	// So I would think that ideally you would want to make sure that the user
	// is not trying to read into the buffer anything larger than the acutal 
	// filesize or even the max path length but every symlink read call is 
	// reading 4097 bytes which is 4x the max size. Why?
    memzero(buf, sizeof(buf));

	strncpy(buf, symlink->content, user_size);
	if (buf == NULL){
		return -EIO;
	}
	
	returnValue = 0;
	
	updateTimes(symlink, TRUE, FALSE, FALSE);
	return returnValue;
}

/*********************************
 *****                       *****
 ***** ACCESS and ATTRIBUTES *****
 *****                       *****
 *********************************/

/*
 * grayfs_chmod - Change the mode (aka permissions) of the file object
 * See chmod(2) man page for details.
 */
// COMPLETE AND TESTED

static int grayfs_chmod(const char *path, mode_t mode,
                        struct fuse_file_info *fi)
{
	// TODO (Phase 5) --> Implement changing the flags!!!
	// NOTE: Complete but needs testing
	/**
	 * A unique behavior of Linux is that you cannot chmod a link. When you 
	 * chmod a link, it changes the privelges of the target file/directory, not
	 * the link itself. This program behavior similarly. 
	 * 
	 * Although the changing of the file permissions behaves similarly, because
	 * the access measures do not track the permissions (default to 0), the 
	 * change in permissions is not honored. We will need to implement flag 
	 * checking for this to work. Still working through that with Dr. Ebling.
	 */
	int returnValue = -1;
	char path_copy [GRAY_MAX_PATHLENGTH];
	strncpy(path_copy, path, GRAY_MAX_PATHLENGTH);

	if (path_copy == NULL){
		return -ENOENT;
	}
	
	struct gray_fobj *file = getFileObject(&root, path_copy);
	
	if (file == NULL){
		return -ENOENT;
	}
	if (file->type == GrayDir){
		file->mode = S_IFDIR | mode;
	}
	else if(file->type == GrayFile){
        file->mode = S_IFREG | mode;
	}
	else if (file->type == GrayDev){
		file->mode = S_IFCHR | mode;
	}
	else if (file->type == GrayLink){
    	file->mode = S_IFLNK | mode;
	}
	else{
		return -ENOTSUP;
	}

	returnValue = 0;
	updateTimes(file, TRUE, TRUE, TRUE);
	
	return returnValue;
}

/*
 * grayfs_chown - Change the owner and group of the file object
 * See chown(2) man page for details.
 */
// COMPLETE AND TESTED
static int grayfs_chown(const char *path, uid_t uid, gid_t gid,
                        struct fuse_file_info *fi)
{
	// TODO (Phase 5)
	// uid_t user_id;                    // User ID of the file object's owner
    // gid_t group_id;                   // Group ID of the file object's group

	int returnValue = -1;
	char path_copy [GRAY_MAX_PATHLENGTH];
	strncpy(path_copy, path, GRAY_MAX_PATHLENGTH);

	if (path_copy == NULL){
		return -EBADFD;
	}

	struct gray_fobj *file = getFileObject(&root, path_copy);

	if (file == NULL){
		return -ENOENT;
	}

	file->user_id = uid;
	file->group_id = gid;

	returnValue = 0;
	updateTimes(file, TRUE, TRUE, TRUE);

	return returnValue;
}

/*
 * grayfs_utimens - Update the last access and modification times of the file
 * See the utime(2) man page for details.
 */
// COMPLETE AND TESTED
static int grayfs_utimens(const char *path, const struct timespec tv[2],
                   struct fuse_file_info *fi) {
	// TODO (Phase 5)
	int returnValue = -ENOTSUP;
	char path_copy [GRAY_MAX_PATHLENGTH];
	strncpy(path_copy, path, GRAY_MAX_PATHLENGTH);
	if (path_copy == NULL){
		return -EBADFD;
	}

	struct gray_fobj *file = getFileObject(&root, path_copy);
	if (file == NULL){
		return -ENONET;
	}
	time_t time = (time_t) tv;
	file->atime = time;
	file->mtime = time;
	returnValue = 0;
	updateTimes(file, TRUE, TRUE, FALSE);
	return returnValue;
}

/*
 * This structure is used by the FUSE library much like the system call
 * table in the system call handler in Pintos to figure out which
 * functions know how to handle which file system requests.
 */
static const struct fuse_operations grayfs_oper = {
	.init       = grayfs_init,
	.getattr	= grayfs_getattr,
	.access     = grayfs_access,
	.mkdir      = grayfs_mkdir,
	.rmdir      = grayfs_rmdir,
	.readdir	= grayfs_readdir,
	.create     = grayfs_create,
	.truncate   = grayfs_truncate,
	.open		= grayfs_open,
	.read		= grayfs_read,
	.write      = grayfs_write,
	.unlink     = grayfs_unlink,
	.rename     = grayfs_rename,
	.mknod      = grayfs_mknod,
	.link       = grayfs_link,
    .symlink    = grayfs_symlink,
	.readlink   = grayfs_readlink,
	.chown      = grayfs_chown,
	.chmod      = grayfs_chmod,
	.utimens    = grayfs_utimens,
};

static void showUsageMessage(const char *programName)
{
	printf("Usage: %s [options] <mountpoint>\n\n", programName);
	printf("FUSE supported options:");
	printf("  -d runs in debug mode\n");
	printf("  -s runs with a single thread (highly recommended for CS481)\n");
	printf("  -f runs in the foreground (highly recommended for CS481)\n");
	printf("\n");
}

/*
 * Phase 5
 * The main function for grayfs has been written for you. No changes required.
 */
int main(int argc, char *argv[])
{
	int ret;
	struct fuse_args args = FUSE_ARGS_INIT(argc, argv);

	printf("GrayFS Booting...\n");

	/* Parse options */
	if (fuse_opt_parse(&args, &options, option_spec, NULL) == -1)
		return 1;

	/* Show help messages. */
	if (options.show_help) {
		showUsageMessage(argv[0]);
		assert(fuse_opt_add_arg(&args, "--help") == 0);
		args.argv[0][0] = '\0';
	}
	// I added this line
	//fuse_opt_add_arg(&args, "-d");
	fuse_opt_add_arg(&args, "-o");
	fuse_opt_add_arg(&args, "attr_timeout=0");
	fuse_opt_add_arg(&args, "-o");
	fuse_opt_add_arg(&args, "entry_timeout=0");
	fuse_opt_add_arg(&args, "-o");
	fuse_opt_add_arg(&args, "allow_other");
	//fuse_opt_add_arg(&args, "-o");
	//fuse_opt_add_arg(&args, "no_cache");
	
	// ----------------
	ret = fuse_main(args.argc, args.argv, &grayfs_oper, NULL);
	fuse_opt_free_args(&args);

	return ret;
}
