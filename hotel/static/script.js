// some js tweaking to show prices and days "in real time" without AJAX
// price and days also are available as booking instance methods, but this would be available after adding it to db
// used in booking creation and edits
function get_days_and_price(prices) {
    var date1;
    var date2;

    $("[name='check_in']").on("change", function(event) {
         var date = new Date(event.target.value);
         date1 = date;
    } );

    $("[name='check_out']").on("change", function(event) {
        var date = new Date(event.target.value);
        date2 = date;
    } );

    $("[name='check_in'], [name='check_out']").on("change", function(event) {
        if( !isNaN(date1) && !isNaN(date2) ) {
            days = (date2-date1)/(60*60*24*1000)
            if( days>0 ) {
                $("#days").text(days);
            } else {
                $("#days").text('Invalid date');
            }
        }
    } );

    $("[name='check_in'], [name='check_out'], [name='rooms']").on("change", function(event) {
        var selectedValues = $("[name='rooms'] option:selected").text();
        var countA = 0;
        var countB = 0;
        var countC = 0;
        var countD = 0;
        for (var s of selectedValues) {
            if (s == 'A') {countA = countA + 1}
            if (s == 'B') {countB = countB + 1}
            if (s == 'C') {countC = countC + 1}
            if (s == 'D') {countD = countD + 1}
        }
        dz = $("#days").text();
        var intdz = parseInt(dz);
        if (!isNaN(intdz) && dz === '' + intdz){
            total_price = (prices['A']*countA + prices['B']*countB + prices['C']*countC + prices['D']*countD)*dz;
            $("#price").text(total_price);
        }
    } );
}
