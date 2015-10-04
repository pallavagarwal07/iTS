var MongoClient = require('mongodb').MongoClient;
MongoClient.connect("mongodb://172.17.0.1:27017/codes", function(err, db) {
  if(!err) {
    console.log("We are connected");
  }
var collection = db.collection('records');
doc1 = {
'name': 'pallav',
'surname': 'agarwal'
};
  collection.insert(doc1, function(err){if(!err)console.log("Inserted!");});
});
