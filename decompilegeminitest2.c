#include <stdio.h>
#include <stdlib.h>     // For exit()
#include <stdint.h>     // For uint8_t, uint16_t types
#include <errno.h>      // For perror() to report file errors
#include <string.h>     // For memcpy (though not strictly needed for manual extraction)
#include <iostream>

// Define the structure - used for organizing data after reading
typedef struct{
	char identifier;
	uint8_t minutes;
	uint8_t seconds;
	uint8_t id;
	uint16_t milisecond;
	int16_t value;
}can_data_struct;

// Define the expected size of one record in the file (based on STM32's memcpy)
#define RECORD_SIZE_IN_FILE 8

int main() {
    //char *filenamenya;
    //std::cout << "Nama file : ";
    //std::cin >> filenamenya;
    // --- Configuration ---
    // !!! IMPORTANT: Change this to the actual name/path of your log file !!!
    //const char *filename = "23_47_46_16012000.txt"; // <-- CHANGE THIS
     const char *filename = "16_05_30_01012000.txt";
    // ---------------------

    FILE *infile; // File pointer
    unsigned char raw_record[RECORD_SIZE_IN_FILE]; // Buffer to hold raw bytes for one record
    can_data_struct decoded_record; // Struct to hold the interpreted data
    size_t records_read = 0; // Counter for the number of records processed
    size_t items_read_this_time = 0; // To store the return value of fread

    // --- Print sizeof information for debugging ---
    printf("DEBUG: sizeof(can_data_struct) on this computer: %zu bytes\n", sizeof(can_data_struct));
    printf("DEBUG: Expected record size from file: %d bytes\n", RECORD_SIZE_IN_FILE);
    if (sizeof(can_data_struct) != RECORD_SIZE_IN_FILE) {
         printf("WARNING: Struct size mismatch between compiler and expected file format!\n");
         printf("         Attempting manual extraction based on %d bytes per record.\n", RECORD_SIZE_IN_FILE);
    }
    printf("\n");


    // --- Open the binary log file for reading ---
    infile = fopen(filename, "rb");

    // --- Check if the file opened successfully ---
    if (infile == NULL) {
        perror("Error opening file"); // Prints the system error message
        fprintf(stderr, "Failed to open file: %s\n", filename);
        fprintf(stderr, "Please check the filename/path and file permissions.\n");
        return 1; // Indicate failure
    }

    printf("Successfully opened file: %s\n", filename);
    printf("Reading records (%d bytes each)...\n", RECORD_SIZE_IN_FILE);
    printf("--------------------------------------------------\n");

    // --- Read the file record by record (reading raw bytes) ---
    // Read RECORD_SIZE_IN_FILE bytes at a time into raw_record buffer
    while ((items_read_this_time = fread(raw_record, 1, RECORD_SIZE_IN_FILE, infile)) == RECORD_SIZE_IN_FILE) {
        records_read++; // Increment the record counter

        decoded_record.identifier = raw_record[0];
        decoded_record.minutes = raw_record[1];
        decoded_record.seconds = raw_record[2];
        decoded_record.id = (uint8_t)raw_record[3];
        decoded_record.milisecond = (uint16_t)raw_record[4] | ((uint16_t)raw_record[5] << 8);
        decoded_record.value = (int16_t)raw_record[6] | ((int16_t)raw_record[7] << 8);


        // --- Format and print the data from the 'decoded_record' struct ---
        printf("Record %zu: H=%c M=%u S=%u MS=%u ID=%02u Val=%d\n",
               records_read,
               (char)decoded_record.identifier,
               (unsigned int)decoded_record.minutes,
               (unsigned int)decoded_record.seconds,
               decoded_record.milisecond,
               (uint8_t)decoded_record.id,
               (int16_t)decoded_record.value);
    }

    // --- After the loop ---
    printf("--------------------------------------------------\n");

    // Check if the loop stopped because of an error or end-of-file
    if (ferror(infile)) {
        perror("Error reading file");
        fprintf(stderr, "An error occurred while reading the file.\n");
    } else if (feof(infile)) {
        printf("Reached end of file.\n");
        // Check if the last read was incomplete (items_read_this_time will be < RECORD_SIZE_IN_FILE but > 0)
        if(items_read_this_time > 0) {
             fprintf(stderr, "Warning: Last record in file appears incomplete (%zu bytes read).\n", items_read_this_time);
        }
    } else {
         // This case means fread returned 0 without EOF or error being set immediately,
         // or items_read_this_time was non-zero but less than expected (handled above).
         fprintf(stderr, "File reading stopped unexpectedly.\n");
    }

    printf("Total complete records successfully read and printed: %zu\n", records_read);

    // --- Close the file ---
    fclose(infile);

    return 0; // Indicate successful execution
}
