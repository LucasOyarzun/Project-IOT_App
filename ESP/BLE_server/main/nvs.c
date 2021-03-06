#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "nvs.h"

int Write_NVS(int32_t data, int key) {
    // Initialize NVS
    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES) {
        // NVS partition was truncated and needs to be erased
        // Retry nvs_flash_init
        ESP_ERROR_CHECK(nvs_flash_erase());
        err = nvs_flash_init();
    }
    ESP_ERROR_CHECK( err );

    // Open
    // printf("Opening NVS .. ");
    nvs_handle_t my_handle;
    err = nvs_open("Storage", NVS_READWRITE, &my_handle);
    if (err != ESP_OK) {
        printf("Error (%d) opening NVS handle!\n", err);
        return -1;
    } else {
        // printf("Done\n");
        // // Write
        // printf("Updating restart counter in NVS ... ");
        switch (key)
        {
            case 1:
                err = nvs_set_i32(my_handle, "status", data);
                break;
            case 2:
                err = nvs_set_i32(my_handle, "ID_Protocol", data);
                break;
            case 3:
                err = nvs_set_i32(my_handle, "BMI270_Sampling", data);
                break;
            case 4:
                err = nvs_set_i32(my_handle, "BMI270_Acc_Sensibility", data);
                break;
            case 5:
                err = nvs_set_i32(my_handle, "BMI270_Gyro_Sensibility", data);
                break;
            case 6:
                err = nvs_set_i32(my_handle, "BME688_Sampling", data);
                break;
            case 7:
                err = nvs_set_i32(my_handle, "Discontinuous_Time", data);
                break;
            case 8:
                err = nvs_set_i32(my_handle, "Port_TCP", data);
                break;
            case 9:
                err = nvs_set_i32(my_handle, "Port_UDP", data);
                break;
            case 10:
                err = nvs_set_i32(my_handle, "Host_Ip_Addr", data);
                break;
            default:
                printf("ERROR key");
                break;
        }
        printf((err != ESP_OK) ? "Failed in NVS!\n" : "Done\n");
        // printf("Committing updates in NVS ... ");
        err = nvs_commit(my_handle);
        printf((err != ESP_OK) ? "Failed!\n" : "Done\n");
        // Close
        nvs_close(my_handle);
    }
    fflush(stdout);
    return 0;
}

esp_err_t Write_NVS_str(char* data, int key) {
    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        err = nvs_flash_init();
    }
    ESP_ERROR_CHECK( err );

    nvs_handle_t my_handle;
    err = nvs_open("Storage", NVS_READWRITE, &my_handle);
    if (err != ESP_OK) {
        printf("Error (%d) opening NVS handle!\n", err);
        return -1;
    } else {
        switch (key) {
            case 11:
                err = nvs_set_str(my_handle, "Ssid", data);
                break;
            case 12:
                err = nvs_set_str(my_handle, "Pass", data);
                break;
            default:
                printf("ERROR key");
                break;
        }
        err = nvs_commit(my_handle);
        nvs_close(my_handle);
    }
    fflush(stdout);
    return err;
}

esp_err_t Read_NVS(int32_t* data, int key){
    // Initialize NVS
    esp_err_t err = nvs_flash_init();
    ESP_ERROR_CHECK( err );

    // Open
    // printf("\n");
    // printf("Opening Non-Volatile Storage (NVS) handle... ");
    nvs_handle_t my_handle;
    err = nvs_open("Storage", NVS_READWRITE, &my_handle);
    if (err != ESP_OK) {
        printf("Error (%d) opening NVS handle!\n", err);
        return -1;
    } else {
        // printf("Done\n");

        // // Read
        // printf("Reading from NVS ... ");
        switch (key)
        {
            case 1:
                err = nvs_get_i32(my_handle, "status", data);
                break;
            case 2:
                err = nvs_get_i32(my_handle, "ID_Protocol", data);
                break;
            case 3:
                err = nvs_get_i32(my_handle, "BMI270_Sampling", data);
                break;
            case 4:
                err = nvs_get_i32(my_handle, "BMI270_Acc_Sensibility", data);
                break;
            case 5:
                err = nvs_get_i32(my_handle, "BMI270_Gyro_Sensibility", data);
                break;
            case 6:
                err = nvs_get_i32(my_handle, "BME688_Sampling", data);
                break;
            case 7:
                err = nvs_get_i32(my_handle, "Discontinuous_Time", data);
                break;
            case 8:
                err = nvs_get_i32(my_handle, "Port_TCP", data);
                break;
            case 9:
                err = nvs_get_i32(my_handle, "Port_UDP", data);
                break;
            case 10:
                err = nvs_get_i32(my_handle, "Host_Ip_Addr", data);
                break;
            default:
                printf("ERROR key");
                break;
        }
        switch (err) {
            case ESP_OK:
                //printf("Done\n");
                // printf("Value Data = %d\n", *data);
                break;
            case ESP_ERR_NVS_NOT_FOUND:
                printf("The value is not initialized yet!\n");
                break;
            default :
                printf("Error (%d) reading!\n", err);
        }
        // printf("Committing updates in NVS ... ");
        // printf((err != ESP_OK) ? "Failed!\n" : "Done\n");
        // Close
        nvs_close(my_handle);
    }
    fflush(stdout);
    return err;
}

esp_err_t Read_NVS_str(char* data, int key, size_t *length){
    // Initialize NVS
    esp_err_t err = nvs_flash_init();
    ESP_ERROR_CHECK( err );

    // Open
    // printf("\n");
    // printf("Opening Non-Volatile Storage (NVS) handle... ");
    nvs_handle_t my_handle;
    err = nvs_open("Storage", NVS_READWRITE, &my_handle);
    if (err != ESP_OK) {
        printf("Error (%d) opening NVS handle!\n", err);
        return -1;
    } else {
        switch (key)
        {
            case 11:
                err = nvs_get_str(my_handle, "Ssid", data, length);
                break;
            case 12:
                err = nvs_get_str(my_handle, "Pass", data, length);
                break;

            default:
                printf("ERROR key");
                break;
        }
        switch (err) {
            case ESP_OK:
                break;
            case ESP_ERR_NVS_NOT_FOUND:
                printf("The value is not initialized yet!\n");
                break;
            default :
                printf("Error (%d) reading string!\n", err);
        }
        nvs_close(my_handle);
    }
    fflush(stdout);
    return err;
}

