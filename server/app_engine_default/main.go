package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

// init is called before the main function.
func init() {
	// Register the handler for the root path ("/").
	http.HandleFunc("/", handler)
}

// handler responds to HTTP requests with a simple "Hello, World!" message.
func handler(w http.ResponseWriter, r *http.Request) {
	// Log the incoming request path.
	log.Printf("Received request for: %s", r.URL.Path)

	// Write the "Hello, World!" message to the response.
	fmt.Fprintln(w, "Hello, World! (from App Engine default service)")
}

// main is the entry point for the application.
func main() {
	// App Engine sets the PORT environment variable.
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080" // Default port for local development
		log.Printf("Defaulting to port %s", port)
	}

	log.Printf("Listening on port %s", port)
	// Start the HTTP server.
	// log.Fatal will print the error and exit if the server fails to start.
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%s", port), nil))
}
