function setLangSubmit(event) {
    var $form, $this;

    $this = $(event.currentTarget);
    $form = $this.closest('form#set-lang-form');
    $form.find('input[name="language"]').val($this.data('lang'));
    $form.submit();
};

$(document).ready(function(){
    var $setLangForm;
    $setLangForm = $('form#set-lang-form');
    $setLangForm.on('click', '.dropdown-menu li', setLangSubmit);
});
