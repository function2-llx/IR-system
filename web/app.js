const express = require('express')
const path = require('path')
const app = express()
var bodyParser = require('body-parser')

app.use(express.static(path.join(__dirname, 'static')))
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({//处理以form表单的提交
    extended: true
}));

const { Client } = require('@elastic/elasticsearch')
const client = new Client({node: 'http://localhost:9200'})

app.post('/search', function(req, res) {
    let data = JSON.parse(req.body.data);
    let tokens = data.tokens;
    let constraints = data.constraints;
    mappedTokens = []
    tokens.forEach((token_pos) => {
        token_pos = token_pos.filter(x => x);
        mappedTokens.push(token_pos.join('_'));
    })
    let query = mappedTokens.filter(x => x).join(' ');
    if (!query) {
        res.json({
            total: 0,
            hits: [],
        });
        return;
    }

    let must = [{match: { content: query }}];
    let must_not = [];
    let lnear = (token1, token2) => { return {match_phrase: {content: [token1, token2].join(' ')}}; };
    let rnear = (token1, token2) => { return {match_phrase: {content: [token2, token1].join(' ')}}; };
    let near = (token1, token2) => {
        return {
            bool: {
                should: [
                    lnear(token1, token2),
                    rnear(token1, token2)
                ]
            }
        };
    };
    constraints.forEach(([id1, id2, r]) => {
        let ids = [id1, id2].filter(id => {
            id = parseInt(id) - 1;
            if (id < 0 || mappedTokens.length <= id) return false;
            return mappedTokens[id];
        });
        if (ids.length < 2) return;
        [token1, token2] = ids.map(id => mappedTokens[id - 1]);
        switch (r) {
            case '相邻': must.push(near(token1, token2));
            break;
            case '不相邻': must_not.push(near(token1, token2));
            break;
            case '左邻': must.push(lnear(token1, token2));
            break;
            case '不左邻': must_not.push(lnear(token1, token2));
            break;
            case '右邻': must.push(rnear(token1, token2));
            break;
            case '不右邻': must_not.push(rnear(token1, token2));
            break;
        }
    });
    client.search({
        index: 'docs',
        body: {
            from: data.from,
            query: {
                bool: {
                    must: must,
                    must_not: must_not,
                }
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
            return {
                score: hit._score,
                content: content,
            }
        })
        res.json({
            total: total,
            hits: hits,
        })
    });
})


let port = 8080;
app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
})