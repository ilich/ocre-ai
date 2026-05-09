## MongoDB

### Seed database

```bash
make seed
make embed
```

### Create Vector Index

```js
db.coins.createSearchIndex(
    "coins_text_search",
    {
      mappings: {
        dynamic: false,
        fields: {
          record_id:    [{ type: "string", analyzer: "lucene.standard" }],
          title:        [{ type: "string", analyzer: "lucene.standard" }],
          description:  [{ type: "string", analyzer: "lucene.standard" }],
          authority:    [{ type: "string", analyzer: "lucene.standard" }],
          denomination: [{ type: "string", analyzer: "lucene.standard" }],
          manufacturer: [{ type: "string", analyzer: "lucene.standard" }],
          material:     [{ type: "string", analyzer: "lucene.standard" }],
          object_type:  [{ type: "string", analyzer: "lucene.standard" }],
        }
      }
    }
  );

db.runCommand({
  createSearchIndexes: "coins",
  indexes: [
    {
      name: "coins_vector_search",
      type: "vectorSearch",
      definition: {
        fields: [
          {
            type: "vector",
            path: "embedding",
            numDimensions: 1536,
            similarity: "cosine"
          }
        ]
      }
    }
  ]
});
```

### Backup and restore MongoDB

```bash
mongodump \
  --uri="mongodb://localhost:27017/?directConnection=true" \
  -db="ocre_ai" \
  --out="./backup"
```

```bash
mongorestore \
  --uri="mongodb://localhost:27017/?directConnection=true" \
  --db="ocre_ai" \
  "./backup/ocre_ai"
```
