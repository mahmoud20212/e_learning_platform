$(document).ready(() => {
    // Toggle menu in mobile
    const navLinks = document.querySelector('.nav-links');
    function onToggleMenu(e) {
        e.name = e.name === 'menu' ? 'close' : 'menu';
        navLinks.classList.toggle('top-[60px]');
    }

    // Toggle filter list
    $('.btn-toggle-filter-list').click((e) => {
        const listId = e.target.getAttribute('aria-controls');
        const filterSection = $(`#${listId}`);

        // Toggle the filter section
        filterSection.slideToggle();

        // Toggle the plus and minus icons based on aria-expanded attribute
        const plusIcon = filterSection.prev().find('.plus-icon');
        const minusIcon = filterSection.prev().find('.minus-icon');

        const isExpanded = e.target.getAttribute('aria-expanded') === 'true';

        if (isExpanded) {
            plusIcon.hide();
            minusIcon.show();
            e.target.setAttribute('aria-expanded', 'false');
        } else {
            plusIcon.show();
            minusIcon.hide();
            e.target.setAttribute('aria-expanded', 'true');
        }
    });

    // Toggle sort menu
    $('#menu-sort-button').click(() =>{
        $('#menu-sort').slideToggle();
    });

    // Toggle sidebar filter
    $('#btn-filter-mobile').click(() =>{
        $('#sidebar-filter-mobile').removeClass('hidden');
    });
    $('#menu-sort-close-button').click(() =>{
        $('#sidebar-filter-mobile').addClass('hidden');
    });

    // Toggle active in links
    $('.nav-links ul li > a').click(function () {
        $(this).addClass('active').parent().siblings().find('a').removeClass('active');
    });
    
});