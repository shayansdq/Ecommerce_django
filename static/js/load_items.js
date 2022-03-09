function rep(item){
    return {"name":item.name.replace(/ /g,'-'),"price":item.price,"count":item.count}
}
loadedCartItems = '{{ request.session.loaded_items }}'.replace(/&#x27;/g,'"')
parseloadedCartItems = JSON.parse(loadedCartItems)
items = JSON.stringify(parseloadedCartItems.map(rep))
sessionStorage.setItem('shoppingCart', items);