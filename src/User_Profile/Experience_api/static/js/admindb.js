
document.addEventListener('DOMContentLoaded', function() {
    var contentContainer = document.querySelector('.contentcontainer');
    var ele='a';
    acms=JSON.parse(acms);
    users=JSON.parse(users);
    function createContentDiv() {
        var content = document.createElement('div');
        content.className = 'content'; // Set the class to "content"
        return content;
    }

    function showAcms() {
        ele='a';
        contentContainer.innerHTML = '';
        var content = document.createElement('div');
        content.className = 'contenttitle';
        content.innerHTML = `<p>Email Id</p><p>Name</p><p>Contact No</p>`;
        contentContainer.appendChild(content);
        acms.forEach(function(acm) {
            var content = createContentDiv();
            content.innerHTML = `<p><a href="acmmod/?acmid=${acm.acmid}&ap=0">${acm.acmid}</a></p><p>${acm.name}</p><p>${acm.phno}</p>`;
            contentContainer.appendChild(content);
        });
    }

    // Function to display Users content
    function showUsers() {
        ele='u';
        contentContainer.innerHTML = '';
        
        var content = document.createElement('div');
        content.className = 'contenttitle';
        content.innerHTML = `<p>Email Id</p><p>Name</p><p>Contact No</p>`;
        contentContainer.appendChild(content);
        users.forEach(function(user) {
            var content = createContentDiv();
            content.innerHTML = `<p><a href="showuser/?mailid=${user.mailid}&ap=0">${user.mailid}</a></p><p>${user.name}</p><p>${user.phno}</p>`;
            contentContainer.appendChild(content);
        });
    }

    // Attach click event handlers to the buttons
    document.getElementById('acmsButton').addEventListener('click', showAcms);
    document.getElementById('usersButton').addEventListener('click', showUsers);
    showAcms();


    var searchbar=document.getElementById("searchid");
    searchbar.addEventListener("input",function(){
        var searchText = searchbar.value.toLowerCase();
        contentContainer.innerHTML = '';
        if (ele==='a'){
            acms.forEach(function (item) {
                if (item.acmid.toLowerCase().includes(searchText) || item.name.toLowerCase().includes(searchText) ||  (item.phno && item.phno.toLowerCase().includes(searchText))) {
                    var content = createContentDiv();
                    content.innerHTML = `<p><a href="acmmod/?acmid=${item.acmid}&ap=0">${item.acmid}</a></p><p>${item.name}</p><p>${item.phno}</p>`;
                    contentContainer.appendChild(content);
                }
            });
        }
        else{
            users.forEach(function (item) {
                if (item.mailid.toLowerCase().includes(searchText) || item.name.toLowerCase().includes(searchText) || (item.phno && item.phno.toLowerCase().includes(searchText))) {
                    var content = createContentDiv();
                    content.innerHTML = `<p><a href="showuser/?mailid=${item.mailid}&ap=0">${item.mailid}</a></p><p>${item.name}</p><p>${item.phno}</p>`;
                    contentContainer.appendChild(content);
                }
            });
        } 
        })

});
