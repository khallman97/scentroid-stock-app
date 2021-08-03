import { render, fireEvent } from '@testing-library/react';
import { configure,  } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import Home from './Home'
configure({ adapter: new Adapter() });


/* Testing of the home component */
describe("Home Component" , () => {

    /*Check that the option div is in the doc upon rendered */
    test("Options div is in the document" , () => {
        const component = render(<Home/>);
        const optionsDiv = component.getByTestId("date-form-div")
        expect(optionsDiv).toBeInTheDocument()
    })

    /*Check that the option div is in the doc upon rendered */
    test("Default value for radio is UTC and change on click" , () => {
        const component = render(<Home/>);
        const radioButUTC = component.getByTestId("radio-button-UTC")
        expect(radioButUTC.checked).toEqual(true)
    
        //Check the checked value moves to another radio button when clicked
        const radioButTOR = component.getByTestId('radio-button-TOR');
        fireEvent.click(radioButTOR, { target: { checked: true }});
        expect(radioButTOR.checked).toEqual(true);
        expect(radioButUTC.checked).toEqual(false);
    })

    /* Check the dates have no dates as default values */
    test("Default value for start and end date are empty" , () => {
        const component = render(<Home/>);
        const sDateInput = component.getByTestId('sdate-input');
        expect(sDateInput.value).toBe("")

        const eDateInput = component.getByTestId('edate-input');
        expect(eDateInput.value).toBe("")

    })
})

