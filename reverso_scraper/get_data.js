// reverso_scraper/get_data.js

const Reverso = require('./reverso.js');

async function fetchData() {
    const args = process.argv.slice(2);
    const [functionName, text, source, target] = args;

    if (!functionName || !text || !source) {
        console.log(JSON.stringify({ ok: false, message: 'Argumentos insuficientes' }));
        process.exit(1);
    }

    const reverso = new Reverso();

    try {
        let result;
        if (functionName === 'context') {
            result = await reverso.getContext(text, source, target);
        } else {
            result = { ok: false, message: `Função '${functionName}' não suportada neste script.` };
        }

        console.log(JSON.stringify(result));

    } catch (error) {
        console.log(JSON.stringify({ ok: false, message: error.message }));
        process.exit(1);
    }
}

fetchData();