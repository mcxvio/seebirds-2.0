$(document).ready(function() {
    var items = new Bloodhound({
        datumTokenizer: function (datum) {
            return Bloodhound.tokenizers.whitespace(datum.value);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: "/data_taxaspecies",
            filter: function (data) {
                return $.map(data.response.taxa, function (taxon) {
                    var species = taxon.comName || taxon.sciName

                    return {
                        value: species + " (" + taxon.speciesCode + ")"
                        ,family: taxon.familyComName
                        ,order: taxon.order
                    };
                });
            }
        }
    });

    // initialize the bloodhound suggestion engine
    items.initialize();

    // instantiate the typeahead UI
    $('#prefetch-find .typeahead').typeahead(
        {
            hint: true,
            highlight: true,
            minLength: 1
        },
        {
            name: 'engine',
            displayKey: 'value',
            source: items.ttAdapter(),
            templates: {
                empty: [
                "<li class='empty-message'>Unable to find any matching results.</li>"
                ].join('\n'),
                suggestion: function(data) {
                  return "<li><a href='/taxa/" + data.value.replace("'", "&#39;") + "/" + data.family + "/" + data.order + "'>" + data.value + "</a></li>";
                }
            }
    });
});
