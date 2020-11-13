const express = require('express')
const path = require('path')
const app = express()
var bodyParser = require('body-parser')

app.use(express.static(path.join(__dirname, 'static')))
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({//处理以form表单的提交
    extended: true
}))

const { Client } = require('@elastic/elasticsearch')
const client = new Client({
    node: 'http://localhost:9200',
})

app.post('/search', function(req, res) {
    let tokens = req.body.tokens;
    console.log(tokens);
    mapped_tokens = []
    tokens.forEach((token_pos) => {
        token_pos = token_pos.filter(x => x);
        if (token_pos.length > 0) {
            mapped_tokens.push(token_pos.join('_'));
        }
    })
    let query = mapped_tokens.join(' ');
    console.log(query);
    if (!query) return;
    client.search({
        index: 'docs',
        body: {
            from: req.body.from,
            query: {
                match: { content: query }
            },
            highlight: {
                pre_tags: ["<b>"],
                post_tags: ["</b>"],
                fields: {
                    content: {}
                },
                fragment_size: 0,
            }
        }
    }, (err, results) => {
        if (err) {
            console.log(err);
            res.json({
                msg: "出错力",
            });
            return;
        }
        let hits = results.body.hits;
        let total = hits.total.value;
        hits = hits.hits.map(hit => {
            let content = hit.highlight.content[0].split(' ').map(x => {
                x = x.split('_')[0];
                if (x.startsWith('<b>')) x += '</b>';
                return x;
            }).join('');
            console.log(content);
            return {
                score: hit._score,
                content: content,
            }
        })
        console.log(hits);
        res.json({
            total: total,
            hits: hits,
        })
    });
})

app.listen(8080, () => {
  console.log('App listening at port 8080')
})