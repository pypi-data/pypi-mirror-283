export class DropdownComponent {
    constructor(audioDevices, changeAudioSourceCallback) {
        this.toggleDropdown = this.toggleDropdown.bind(this);
        this.handleOutsideClick = this.handleOutsideClick.bind(this);
        this.dropdownMenu = document.querySelector('.dropdownMenu');
        this.audioDevices = audioDevices; 
        this.changeAudioSourceCallback = changeAudioSourceCallback;

        this.init();
    }

    init() {
        this.populateDropdownMenu();
        document.querySelector('.btnDropdown').addEventListener('click', this.toggleDropdown);
        document.addEventListener('click', this.handleOutsideClick);
    }

    toggleDropdown(event) {
        event.preventDefault();
        this.dropdownMenu.style.display = this.dropdownMenu.style.display === 'block' ? 'none' : 'block';
    }

    handleOutsideClick(event) {
        if (this.dropdownMenu && !this.dropdownMenu.contains(event.target) && !event.target.matches('.btnDropdown')) {
            this.dropdownMenu.style.display = 'none';
        }
    }
    
    populateDropdownMenu() {    
        // Populate dropdown menu with available audio input devices
        this.audioDevices.forEach(device => {
            const label = document.createElement('label');
            label.classList.add('dropdownItem');
            const input = document.createElement('input');
            input.type = 'checkbox';
            input.name = 'audioDevice';
            input.value = device.deviceId;
            input.addEventListener('change', this.changeAudioSourceCallback);
            label.appendChild(input);
            label.appendChild(document.createTextNode(device.label || `Microphone (${device.deviceId.substr(0, 6)}...)`));
            this.dropdownMenu.appendChild(label);
        });
    
        // Add system audio option
        const label = document.createElement('label');
        label.classList.add('dropdownItem');
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.name = "system-audio";
        input.value = "system-audio";
        input.addEventListener('change', this.changeAudioSourceCallback);
        label.appendChild(input);
        label.appendChild(document.createTextNode("System audio"));
        this.dropdownMenu.appendChild(label);
    
        // autoselect the first entry:
        const firstInput = document.querySelector('.dropdownItem input');
        firstInput.checked = true;
    }
    
}
