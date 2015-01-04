/**
 * Created by Administrator on 2014/11/28.
 */

function hideTooltip(id) {
    console.log('onload test');
    document.getElementById(id).style.display="none";
}

function showTooltip(id){
    var el = document.getElementById(id);
    el.style.display = "block";
    //el.style.display = el.style.display=="none"?"":"none";
}

function switchPanel(tagId){
    var index = tagId.split('_')[1]

//    if(index=='1'){
//        document.getElementById(tagId).style.borderLeft = '2px solid #E2F0FA';
//    }else if(index=='3'){
//        document.getElementById(tagId).style.borderRight = '2px solid #E2F0FA';
//    }

    console.log(index)
    var content = document.getElementsByClassName('content_data')
    for(var i = 0; i<content.length;i++){
        var nav_tag = document.getElementById('tag_'+ (i+1).toString())
        if(content[i].id!='start_page_'+index.toString()){
            content[i].style.display='none'
            nav_tag.className='unselected'
        }

        else{
            content[i].style.display='block'
            nav_tag.className='selected'

        }
    }
}

function highLight(tagId){
    var obj = document.getElementById(tagId);
    if(obj.className!='selected')
        obj.className = 'high_lighted'
}

function cancelHighLight(tagId) {
    var obj = document.getElementById(tagId);
    if(obj.className!='selected')
        obj.className = 'unselected'
}

