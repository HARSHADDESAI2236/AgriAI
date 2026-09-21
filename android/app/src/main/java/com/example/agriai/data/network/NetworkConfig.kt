package com.example.agriai.data.network

object NetworkConfig {
    /**
     * IMPORTANT: Update this IP to your PC's LAN IP.
     * Use 'ipconfig' (Windows) or 'ifconfig' (Mac/Linux) to find it.
     * Ensure your physical phone is on the same Wi-Fi.
     */
    private const val LAN_IP = "192.168.1.100" // Replace with your actual LAN IP
    const val BASE_URL = "http://$LAN_IP:8000/"
}
