const Reverso = require('./reverso.js');

// Função principal para executar os testes
async function runTests() {
    const args = process.argv.slice(2); // Pega os argumentos da linha de comando
    const [functionToTest, ...params] = args;

    if (!functionToTest) {
        console.error('ERRO: Você precisa especificar qual função testar.');
        console.log('\nUso: node test_reverso.js <funcao> [parametros...]');
        console.log('\nFunções disponíveis: context, translation, synonyms, spell, conjugation');
        console.log('\nExemplo: node test_reverso.js context "a new day" english portuguese');
        process.exit(1);
    }

    const reverso = new Reverso();
    let result;

    console.log(`--- Executando teste para a função: ${functionToTest} ---\n`);

    try {
        switch (functionToTest) {
            case 'context':
                const [text, source, target] = params;
                if (!text || !source || !target) {
                    console.error('Uso para "context": <texto> <idioma_origem> <idioma_destino>');
                    return;
                }
                result = await reverso.getContext(text, source, target);
                break;

            case 'translation':
                const [transText, transSource, transTarget] = params;
                 if (!transText || !transSource || !transTarget) {
                    console.error('Uso para "translation": <texto> <idioma_origem> <idioma_destino>');
                    return;
                }
                result = await reverso.getTranslation(transText, transSource, transTarget);
                break;

            case 'synonyms':
                const [synText, synSource] = params;
                if (!synText || !synSource) {
                    console.error('Uso para "synonyms": <texto> <idioma>');
                    return;
                }
                result = await reverso.getSynonyms(synText, synSource);
                break;
            
            case 'spell':
                const [spellText, spellSource] = params;
                if (!spellText || !spellSource) {
                    console.error('Uso para "spell": <texto> <idioma>');
                    return;
                }
                result = await reverso.getSpellCheck(spellText, spellSource);
                break;

            case 'conjugation':
                const [conjText, conjSource] = params;
                if (!conjText || !conjSource) {
                    console.error('Uso para "conjugation": <verbo> <idioma>');
                    return;
                }
                result = await reverso.getConjugation(conjText, conjSource);
                break;

            default:
                console.error(`Função "${functionToTest}" não reconhecida.`);
                return;
        }

        console.log('✅ Resultado recebido com sucesso:\n');
        // Imprime o objeto JSON de resultado de forma legível
        console.log(JSON.stringify(result, null, 2));

    } catch (error) {
        console.error('🔴 Ocorreu um erro durante o teste:', error);
    }
}

runTests();