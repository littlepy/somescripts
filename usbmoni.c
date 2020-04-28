/* List and monitor USB devices using libudev.
 *
 * gcc -o usbmoni usbmoni.c -ludev
 * ./usbmoni
 */
#include <libudev.h>
#include <stdio.h>
#include <string.h>
#include <sys/mount.h>
#include <sys/stat.h>

#define SUBSYSTEM "block"

static void mount_device(struct udev_device* dev, char mount_point[])
{
    char* devlink;
    const char* mount_prefix = "/mnt/";
    const char* action = udev_device_get_action(dev);
    if (! action)
        action = "exists";
	
    const char* ID_USB_DRIVER = udev_device_get_property_value(dev, "ID_USB_DRIVER");
    const char* ID_FS_TYPE    = udev_device_get_property_value(dev, "ID_FS_TYPE");
    const char* ID_FS_UUID 	  = udev_device_get_property_value(dev, "ID_FS_UUID");
	const char* DEVTYPE       = udev_device_get_property_value(dev, "DEVTYPE");
	const char* DEVLINKS 	  = udev_device_get_property_value(dev, "DEVLINKS");


    if (ID_USB_DRIVER == NULL || DEVTYPE == NULL  || 
		0 != strcmp(ID_USB_DRIVER, "usb-storage") || 
		0 != strcmp(DEVTYPE, "partition")) {
        strcpy(mount_point, "NOTUSBPARTITION");
	    return;
    }
	
	
	devlink = strtok((char*)DEVLINKS, " ");
	
	while (devlink != NULL) {
	    if (strstr(devlink, "by-uuid") != NULL) {
            break;  
        }    
        devlink = strtok(NULL, " ");
	}
	
    
    
    if (ID_FS_UUID != NULL) {
        strcpy(mount_point, mount_prefix);
        strcat(mount_point, ID_FS_UUID);
        mkdir((const char*)mount_point, S_IRWXU);
    }
	
	if (0 == strcmp(action, "add")) {
		mount((const char*)devlink, mount_point, ID_FS_TYPE, 0, "");
	} 
    else if (0 == strcmp(action, "exists")){
        mount((const char*)devlink, mount_point, ID_FS_TYPE, 0, "");
    }
	else if (0 == strcmp(action, "remove")) {
		umount2((const char*)mount_point, 0);
	}
    
    
    printf("action: %s, mount_point: %s, devlink: %s\n", action, mount_point, devlink);
    
}






static void process_device(struct udev_device* dev)
{
    if (dev) {
        if (udev_device_get_devnode(dev)){
            char mount_p[128];
            mount_device(dev, mount_p);
            if (mount_p)
                printf("mount point is: %s\n", mount_p);
        }
        udev_device_unref(dev);
    }
}

static void enumerate_devices(struct udev* udev)
{
    struct udev_enumerate* enumerate = udev_enumerate_new(udev);

    udev_enumerate_add_match_subsystem(enumerate, SUBSYSTEM);
    udev_enumerate_scan_devices(enumerate);

    struct udev_list_entry* devices = udev_enumerate_get_list_entry(enumerate);
    struct udev_list_entry* entry;

    udev_list_entry_foreach(entry, devices) {
        const char* path = udev_list_entry_get_name(entry);
        struct udev_device* dev = udev_device_new_from_syspath(udev, path);
        process_device(dev);
    }

    udev_enumerate_unref(enumerate);
}

static void monitor_devices(struct udev* udev)
{
    struct udev_monitor* mon = udev_monitor_new_from_netlink(udev, "udev");

    udev_monitor_filter_add_match_subsystem_devtype(mon, SUBSYSTEM, "partition");
    udev_monitor_enable_receiving(mon);

    int fd = udev_monitor_get_fd(mon);

    while (1) {
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(fd, &fds);

        int ret = select(fd+1, &fds, NULL, NULL, NULL);
        if (ret <= 0)
            break;

        if (FD_ISSET(fd, &fds)) {
            struct udev_device* dev = udev_monitor_receive_device(mon);
            process_device(dev);
        }
    }
}

int main(void)
{
    struct udev* udev = udev_new();
    if (!udev) {
        fprintf(stderr, "udev_new() failed\n");
        return 1;
    }

    enumerate_devices(udev);
    monitor_devices(udev);

    udev_unref(udev);
    return 0;
}
