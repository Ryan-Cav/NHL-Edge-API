// Connect to the admin database
var adminDb = db.getSiblingDB('admin');

// Create collections
adminDb.createCollection('players');
adminDb.createCollection('teams');

// Create indexes, add users, etc. as needed
