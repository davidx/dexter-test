package main

import (
	"fmt"
	"log"
	"os"
)

func main() {
	// These Println statements should be detected by Dexter
	fmt.Println("Starting application...")
	fmt.Println("Initializing components")
	
	err := initialize()
	if err != nil {
		fmt.Println("Error during initialization:", err)
		os.Exit(1)
	}

	fmt.Println("Application running successfully")
}

func initialize() error {
	// More Println statements
	fmt.Println("Setting up database connection")
	fmt.Println("Loading configuration")
	
	// Use proper logging for comparison
	log.Println("This is using the standard logger")
	
	return nil
}
