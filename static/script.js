import { dom } from './dom.js';
import { downloadsLinks } from './downloadLinks.js';
import { timeInputs } from './timeInputs.js';

(function () {
    const timeInputsObj = new timeInputs(dom.startTimeInput, dom.endTimeInput, dom.timeInputs);
    const downloadLinksObj = new downloadsLinks(dom.downloadLinks);

    // Set time inputs toggle to disabled by default, change it according to checkbox
    timeInputsObj.toggleInputs(false);
    dom.trimToggle.addEventListener('change', e => {
        const isTrimmed = e.target.checked;
        timeInputsObj.toggleInputs(isTrimmed);
        downloadLinksObj.removeOrUpdateQueryStrings(isTrimmed, timeInputsObj.getTime());

    });

    // Update the query strings for download links when changing the time inputs
    dom.timeInputs.forEach(input => {
        input.addEventListener('change', () => {
            downloadLinksObj.updateQueryStrings(timeInputsObj.getTime());
        });
    });

})();
