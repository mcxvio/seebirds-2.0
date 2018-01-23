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
                //"<li class='empty-message'>Unable to find any matching results.</li>"
                "<a href='#' class='list-group-item list-group-item-danger'>Unable to find any matching results.</a>"
                ].join('\n'),
                suggestion: function(data) {
                  //return "<li><a href='/taxa/" + data.value.replace("'", "&#39;") + "/" + data.family + "/" + data.order + "'>" + data.value + "</a></li>";
                  return "<a href='/taxa/" + data.value.replace("'", "&#39;") + "/" + data.family + "/" + data.order + "' class='list-group-item list-group-item-action list-group-item-success'>" + data.value + "</a>";
                }
            }
    });
});
