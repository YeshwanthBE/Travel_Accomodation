document.addEventListener('DOMContentLoaded', function() {
    var filterIcon = document.querySelector('.filtericon');
    var filter = document.querySelector('.filter');
    
    filterIcon.addEventListener('click', function() {
        if (filter.style.opacity === '1') {
            filter.style.opacity = '0';
        } else {
            filter.style.opacity = '1';
        }
    });
});
