# Manipulando o MongoDB com mongosh

Guia prático usando a coleção `comentario` do projeto como exemplo.

## Acessar o shell

**Docker:**
```bash
docker compose exec mongodb mongosh comments
```

**Instalação local:**
```bash
mongosh comments
```

---

## Selecionar o banco de dados

```js
use comments;
```

---

## CREATE — Inserir documentos

Inserir um documento:
```js
db.comentario.insertOne({
  projeto: 1,
  texto: "Muito bom o projeto!",
  curtidas: 0,
  criado_em: new Date(),
  modificado_em: new Date()
})
```

Inserir vários documentos de uma vez:
```js
db.comentario.insertMany([
  { projeto: 1, texto: "Primeira pergunta", curtidas: 0, criado_em: new Date(), modificado_em: new Date() },
  { projeto: 2, texto: "Segunda pergunta",  curtidas: 0, criado_em: new Date(), modificado_em: new Date() }
])
```

---

## READ — Consultar documentos

Buscar todos os documentos:
```js
db.comentario.find()
```

Buscar com filtro (comentários do projeto 1):
```js
db.comentario.find({ projeto: 1 })
```

Buscar com múltiplos filtros:
```js
db.comentario.find({ projeto: 1, curtidas: 0 })
```

Exibir apenas campos específicos (projeção):
```js
db.comentario.find({ projeto: 1 }, { texto: 1, criado_em: 1, _id: 0 })
```

Buscar um único documento:
```js
db.comentario.findOne({ projeto: 2 })
```

Contar documentos:
```js
db.comentario.countDocuments({ projeto: 1 })
```

Ordenar por data de criação (mais recente primeiro):
```js
db.comentario.find().sort({ criado_em: -1 })
```

Limitar resultados:
```js
db.comentario.find().limit(2)
```

---

## UPDATE — Atualizar documentos

Atualizar um campo de um documento:
```js
db.comentario.updateOne(
  { projeto: 1, texto: "Muito bom o projeto!" },
  { $set: { curtidas: 5, modificado_em: new Date() } }
)
```

Atualizar todos os documentos de um projeto:
```js
db.comentario.updateMany(
  { projeto: 1 },
  { $set: { modificado_em: new Date() } }
)
```

Incrementar o valor de um campo:
```js
db.comentario.updateOne(
  { projeto: 1 },
  { $inc: { curtidas: 1 } }
)
```

---

## DELETE — Remover documentos

Remover um documento específico:
```js
db.comentario.deleteOne({ projeto: 1, texto: "Muito bom o projeto!" })
```

Remover todos os documentos de um projeto:
```js
db.comentario.deleteMany({ projeto: 2 })
```

Remover **todos** os documentos da coleção:
```js
db.comentario.deleteMany({})
```

---

## Inspecionar a coleção

Listar todas as coleções do banco:
```js
show collections
```

Ver estatísticas da coleção:
```js
db.comentario.stats()
```

Ver um exemplo de documento (útil para entender o schema):
```js
db.comentario.findOne()
```

---

## Diferença para o SQL

| Operação  | SQL                              | MongoDB (mongosh)                          |
|-----------|----------------------------------|--------------------------------------------|
| Inserir   | `INSERT INTO ...`                | `db.col.insertOne({...})`                  |
| Consultar | `SELECT * FROM ... WHERE ...`    | `db.col.find({...})`                       |
| Atualizar | `UPDATE ... SET ... WHERE ...`   | `db.col.updateOne({filtro}, {$set: {...}})` |
| Remover   | `DELETE FROM ... WHERE ...`      | `db.col.deleteOne({...})`                  |
| Contar    | `SELECT COUNT(*) FROM ...`       | `db.col.countDocuments({...})`             |
