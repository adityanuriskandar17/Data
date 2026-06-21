// ============================================
// MONGODB UNTUK DATA ENGINEERING
// ============================================
// Bahasa Indonesia - Mongo Shell (mongosh)

// --- MEMBUAT DATABASE ---
use de_learning

// --- CREATE COLLECTION ---
db.createCollection("logs")

// --- INSERT DATA ---
db.logs.insertOne({
    timestamp: new Date(),
    level: "INFO",
    message: "Pipeline started",
    service: "etl-service",
    metadata: { user_id: 123, action: "extract" }
})

db.logs.insertMany([
    { timestamp: new Date(), level: "ERROR", message: "Connection timeout", service: "api" },
    { timestamp: new Date(), level: "WARN", message: "High memory usage", service: "worker" },
    { timestamp: new Date(), level: "INFO", message: "Job completed", service: "etl-service" }
])

// --- QUERY DATA ---
// Filter dasar
db.logs.find({ level: "ERROR" })
db.logs.find({ timestamp: { $gte: ISODate("2025-01-01") } })
db.logs.find({ $or: [{ level: "ERROR" }, { level: "WARN" }] })

// Projection
db.logs.find({}, { message: 1, timestamp: 1, _id: 0 })

// --- AGGREGATION PIPELINE ---
db.logs.aggregate([
    { $match: { timestamp: { $gte: ISODate("2025-01-01") } } },
    { $group: { _id: "$level", count: { $sum: 1 } } },
    { $sort: { count: -1 } }
])

// --- INDEXING ---
db.logs.createIndex({ timestamp: -1 })
db.logs.createIndex({ level: 1, timestamp: -1 })
db.logs.createIndex({ "metadata.user_id": 1 })

// --- TTL INDEX (auto-delete setelah 30 hari) ---
db.logs.createIndex({ timestamp: 1 }, { expireAfterSeconds: 2592000 })

// --- CHANGE STREAMS (real-time monitoring) ---
const changeStream = db.logs.watch()
changeStream.on("change", (change) => {
    print("Perubahan terdeteksi:", JSON.stringify(change))
})
