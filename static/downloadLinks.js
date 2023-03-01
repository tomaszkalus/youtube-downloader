class downloadsLinks {
    constructor(links) {
        this.links = links;
    }

    removeOrUpdateQueryStrings(isTrimmed, time){
        if (!isTrimmed){
            this.removeQueryStrings();
        }
        else{
            this.updateQueryStrings(time);
        }
    }


    removeQueryStrings() {
        this.links.forEach(link => {
            link.href = link.href.split('?', 1)[0];
        });
    }

    updateQueryStrings(time) {

        const start = time.start;
        const end = time.end;

        const params = new URLSearchParams({ start: start.join('_'), end: end.join('_') });

        
        this.links.forEach(link => {
            let base_url = link.href.split('?', 1)[0];

            if (base_url.endsWith('/')) {
                base_url = base_url.slice(0, -1);
            }

            link.href = base_url + '?' + params.toString();
        });
    }

}

export { downloadsLinks };