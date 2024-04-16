package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
)

func main() {
 

    requestBody := map[string]interface{}{
        "definition": command,
        "name":       identifier,
        "hidden":     false,
        "autostart": map[string]bool{
            "completed": false,
            "failed":    true,
            "stopped":   false,
        },
    }

    requestBodyJSON, err := json.Marshal(requestBody)
    if err != nil {
        log.Println("[ERROR] failed marshalling request body:", err)
        return "", err
    }

    resp, err := http.Post("http://localhost:5160/api/v0/pipeline/create", "application/json", bytes.NewBuffer(requestBodyJSON))
    if err != nil {
        log.Printf("[ERROR] failed to create pipeline: %s", err)
        return "", err
    }
    defer resp.Body.Close()

    // Decode the response into a map
    var response map[string]interface{}
    if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
        fmt.Println("Error decoding response:", err)
        return "", err
    }

	if id, ok := response["id"].(string); !ok {
		log.PrintF("[DEBUG]: ID not found in response")
			
    } else {

        
    }
}
