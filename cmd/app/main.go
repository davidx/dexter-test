package main

import (
	"fmt"
	"log"
	"os"
)

func main() {
	// These Println statements should be detected by Dexter
	log.Println("Starting application...")
	log.Println("Initializing components")
	
	err := initialize()
	if err != nil {
		log.Println("Error during initialization:", err)
		os.Exit(1)
	}

	log.Println("Application running successfully")
}

func initialize() error {
	// More Println statements
	log.Println("Setting up database connection")
	log.Println("Loading configuration")
	
	// Use proper logging for comparison
	log.Println("This is using the standard logger")
	
	return nil
}
