let stateslist = ['Acre', 'Alagoas', 'Amapa', 'Amazonas', 'Bahia', 'Ceara', 'Distrito Federal', 'Espirito Santo',
                    'Goias', 'Maranhao', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Para', 'Paraiba', 'Parana',
                    'Pernambuco', 'Piaui', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rodonia',
                    'Roraima', 'Santa Catarina', 'Sao Paulo', 'Sergipe', 'Toncantins']
$(function () {
    $("#states").autocomplete({source: stateslist});
});
