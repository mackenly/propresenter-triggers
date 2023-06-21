# ProPresenter Triggers
Trigger actions using ProPresenter notes

## About
ProPresenter Triggers is Python console application that listens for triggers in ProPresenter notes and sends commands to other broadcast tools and equipment. Using the PTDL spec you can define triggers in ProPresenter notes that will be sent to the application. When slides are changed in ProPresenter, the application will parse the notes and send commands to other applications and equipment as defined by the triggers.

## Installation
### Prerequisites
- [Python 3.10+](https://www.python.org/downloads/) or later
- [ProPresenter 7.9](https://renewedvision.com/propresenter/) or later

### Install
1. Clone this repository or download the latest release
2. Install dependencies: `pip install -r requirements.txt`

## Usage
### Configuration
Configure the application by editing the `config.json` file. You can get your PROPRESENTER_API_URL from ProPresenter > Preferences > Network. Don't forget to enable Network and to include the port number in the URL. (e.g. `http://192.168.1.15:1025` or `http://localhost:1025`)

### Run
Run the application by executing `python main.py` in the project directory.

### Create Triggers
Create triggers in ProPresenter slide notes using the PTDL spec. See the [PTDL v0.1 Specification](#ptdl-v01-specification) for details.

### Send Commands via API
This application has a built in REST API that accepts PTDL triggers sent in the body of a POST request. See [Postman Collection](https://documenter.getpostman.com/view/19380446/2s93z3fkm1) for examples/documentation.

## Supported Actions
### `print_to_console`: input (string)
Prints a message to the console. Useful for testing. Accepts a value of type string to print to the console.

### `hello`
Prints "Hello World" to the console. Useful for testing.

## ProPresenter 3rd Party Trigger Definition Language (PTDL) v0.1
ProPresenter 3rd Party Trigger Definition Language (PTDL) is a JSON-based language specification for defining triggers wthin ProPresenter notes. Designed for sending data over the ProPresenter API to listening clients by using the slide notes feature in ProPresenter.

This specification has been created primarily for use with this project, but is designed to be flexible enough to be used by other applications and may evolve over time into a standalone specification.

### PTDL v0.1 Specification
PTDL v0.1 is a valid JSON object with a single property, `triggers`, which is an array of trigger objects. Additional properties may be added to the root object in future versions of PTDL or by other applications.

#### Trigger Object
A trigger object is a JSON object with the following properties:
- `type` (string): The type of trigger. Currently, only `action` is supported.
- `key` (string): The key of the action to trigger. Keys are defined by the listening application. If the key is not recognized by the listening application, the trigger will be ignored.
- `value` (string): The value to pass to the action. This is optional and may be omitted if the action does not require a value. Depending on the action the string can be a number, boolean, string, or JSON object.
- `when_next` (boolean): If `true`, the action will be triggered if the trigger is present on the next slide. If `false` or omitted, the action will be triggered when the slide containing the trigger is shown.

#### Example of PTDL v0.1
```json
{
  "triggers": [
    {
      "type": "action",
      "key": "print_to_console",
      "value": "Test Message"
    },
    {
      "type": "action",
      "key": "hello"
    },
    {
      "type": "action",
      "key": "print_to_console",
      "value": "I'm next.",
      "when_next": true
    }
  ]
}
```

## Contributing
Contributions are welcome! Please open an issue or pull request if you have any suggestions or would like to contribute to this project.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

[ProPresenter](https://renewedvision.com/propresenter/) is a trademark of Renewed Vision which is not affiliated with this project.

[Blackmagic Design](https://www.blackmagicdesign.com/) and [ATEM](https://www.blackmagicdesign.com/products/atemmini) are trademarks of Blackmagic Design which is not affiliated with this project.

## Support This Project
If you find this project useful, please consider supporting it by [sponsoring me on GitHub](https://github.com/sponsors/mackenly).