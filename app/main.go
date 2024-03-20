package main

import (
	"database/sql"
	"encoding/json"

	"log"
	"net/http"
	"sync"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

var (
	mutex      sync.Mutex
	counterVal int
)

type Counter struct {
	Count int `json:"counter"`
}

func initDB() {
	db, err := sql.Open("sqlite3", "counter.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	sqlStmt := `
	CREATE TABLE IF NOT EXISTS counts (id INTEGER PRIMARY KEY, count INTEGER);`

	_, err = db.Exec(sqlStmt)
	if err != nil {
		log.Fatalf("%q: %s\n", err, sqlStmt)
	}
}

func fetchDBValue() int {
	db, err := sql.Open("sqlite3", "counter.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	var count int
	err = db.QueryRow("SELECT count FROM counts WHERE id = 1").Scan(&count)
	if err != nil {
		log.Fatal(err)
	}
	return count
}

func syncCounterToDB() {
	for {
		time.Sleep(5 * time.Second)
		mutex.Lock()
		db, err := sql.Open("sqlite3", "counter.db")
		if err != nil {
			log.Fatal(err)
		}
		defer db.Close()

		_, err = db.Exec("UPDATE counts SET count = ? WHERE id = 1", counterVal)
		if err != nil {
			log.Fatal(err)
		}
		mutex.Unlock()
	}
}

func incrementCounter(w http.ResponseWriter, r *http.Request) {
	mutex.Lock()
	counterVal++
	mutex.Unlock()
	getCounter(w, r)
}

func getCounter(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	mutex.Lock()
	defer mutex.Unlock()
	json.NewEncoder(w).Encode(Counter{Count: counterVal})
}

func main() {
	initDB()
	counterVal = fetchDBValue()
	go syncCounterToDB()

	http.HandleFunc("/click", incrementCounter)
	http.HandleFunc("/counter", getCounter)

	log.Fatal(http.ListenAndServe(":8080", nil))
}
