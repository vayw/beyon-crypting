package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func handler(w http.ResponseWriter, r *http.Request) {
	// Parse query parameters
	params := r.URL.Query()

	param := params.Get("param")
	if param == "" {
		param = "default"
	}

	// print log message
	log.Printf("/handler endpoint with GET param = %s", param)
	// increment request counter

	// writing response
	w.Write([]byte("Thanks"))
}

func counter(w http.ResponseWriter, r *http.Request) {
	// oh, here we go
	w.WriteHeader(http.StatusNotImplemented)
	w.Write([]byte("Sorry :("))
}

func main() {
	// Register the handler function for the /handler endpoint
	ADDRESS := os.Getenv("ADDRESS")
	PORT := os.Getenv("PORT")
	SERVER := fmt.Sprintf("%s%s", ADDRESS, PORT)

	http.HandleFunc("/handler", handler)
	http.HandleFunc("/counter", counter)

	// Start the HTTP server on port 8080
	log.Printf("Server is running on %s", PORT)
	http.ListenAndServe(SERVER, nil)
}
