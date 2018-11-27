
function yesnoCheck() {
    if (document.getElementById('yesCheck').checked) {
        document.getElementById('auction_end').classList.remove("hidden");
		document.getElementById('price_label').innerHTML = "Starting Price";
    }
    else {
		document.getElementById('auction_end').classList.add("hidden");
		document.getElementById('price_label').innerHTML = "Price";
	}
}

$(document).ready(function() {


    $('#contact_form').bootstrapValidator({

        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {

             i_title: {
                validators: {
                     stringLength: {
                        min: 4,
                        max: 50,
                        message:'Please enter at least 4 characters and no more than 50'
                    },
                    notEmpty: {
                        message: 'Please supply your idea title'
                    }
                }
            },
          i_price: {
                validators: {
                    notEmpty: {
                        message: 'Please supply the price of your idea'
                    }
                }
            },
            i_category: {
                validators: {
                    notEmpty: {
                        message: 'Please select the category of your idea'
                    }
                }
            },
          yesno: {
                validators: {
                    notEmpty: {
                        message: 'Please select the whether you want to give your idea for auction'
                    }
                }
            },

            i_description: {
                validators: {
                      stringLength: {
                        min: 10,
                        max: 200,
                        message:'Please enter at least 10 characters and no more than 500'
                    },
                    notEmpty: {
                        message: 'Please supply a description of your idea'
                    }
                    }
                }
            }
        })



        .on('success.form.bv', function(e) {
            $('#success_message').slideDown({ opacity: "show" }, "slow") // Do something ...
                $('#contact_form').data('bootstrapValidator').resetForm();

            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            // Use Ajax to submit form data
            $.post($form.attr('action'), $form.serialize(), function(result) {
                console.log(result);
            }, 'json');
        });

});
