import React, { Component } from 'react'

//Import components 
import {GraphResults} from '../components/GraphResults'

//Import style sheet for pages
import "./Pages.css"

//Material UI imports
import Button from '@material-ui/core/Button';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';


//Axios to handle api requests
import axios from 'axios'

export class Home extends Component {

    /* 
        Constructor for the Home component.
        State is defined here and values represent:
            timezone: the timezone for the date and time DEFAULT: UTC
            startDate: the start date for the data and graph
            endDate: the end date for the data and graph
            data: the data that comes from the api for the selected time and date
    */
    constructor(props) {
        super(props);
        this.state = {  
            timeZone: "UTC",
            startDate: "",
            endDate: "",
            dateData: [],
            priceData: []
        };
    }

    /* 
        Function for handling the submit of the form. Creates and axios POST request to the api using 
        the timezone, startDate and endDate data that is stored in the state. 
    */
    handleSubmit = () => {   
        axios({
            method: 'post',
            url: '/StockData',
            data: {
                timezone: this.state.timeZone,
                startDate: this.state.startDate,
                endDate: this.state.endDate
            }
        }).then(res => {
            this.setState({ 
                dateData: res.data.date_axis,
                priceData: res.data.data_axis
                })
            }
            
        ).catch(err => {
                console.log(err) //console log any errors
                alert("Please enter valid start and end date and ensure the start date is before the end date") //Send alert for missing dates
            }
        );
        
        //event.preventDefault();
    }

    /* 
        Function for handling the change of the time zone controlled 
        by a radio button. Upon the user clicking a different option 
        the state changes to the value entered.
    */
    handleRadioChange = (event) => {
        this.setState({
            timeZone: event.target.value
        })
    }

    /* 
        Function for handling the change of the start date and end date.
        upon user selection it updates the dates within the state 
        according to the field it was entered in (start date or end date)
    */
    handleDateChange = (event) => {
        //Find the id of the event for the date to seperate between the start date and end date inputs
        if( event.target.id == "sdate") {
            this.setState({
                startDate: event.target.value
            })
        } else {
            this.setState({
                endDate: event.target.value
            })
        }
        
    }
    render() {
        return (
            <div>
                {/* Div for the graph, uses the graph result component with the data in the state passed through as props */}
                <div className="graph-div">
                    <GraphResults xrange={this.state.dateData} yrange={this.state.priceData}></GraphResults>
                </div>
                {/* div for the date form, used for the user to select the data then create and API request upon submit */}
                <div className="date-form" data-testid="date-form-div" >
                    <form >
                        {/* Form control group for radio buttons to align buttons, used material UI radiogroup to orginize 
                        radio buttons and retreieve value */}
                        <FormControl component="fieldset">
                        <h4>Time Zone</h4>
                            <RadioGroup data-testid="rad-group" aria-label="Time-Zone" value={this.state.timeZone} name="timezone" onChange={this.handleRadioChange}>
                                <FormControlLabel  value="UTC" control={<Radio inputProps={{"data-testid": `radio-button-UTC`}} />} label="UTC" />
                                <FormControlLabel data-testid="rad-Tor" value="Toronto" control={<Radio inputProps={{"data-testid": `radio-button-TOR`}} />} label="Toronto" />
                                <FormControlLabel data-testid="rad-Tok" value="Tokyo" control={<Radio inputProps={{"data-testid": `radio-button-TOK`}} />} label="Tokyo" />
                            </RadioGroup>
                        </FormControl>
                        {/* Div for the date picker. Using the type datetime-local to get both the date and time the user 
                        enters. Upon entered data it triggers the event to handle the date change and update the state */}
                        <div className="date-picker">
                            <h4>Date Range (GMT)</h4>
                            <Grid container justifyContent="space-around">
                            <TextField
                                
                                id="sdate"
                                label="Start Date"
                                type="datetime-local"
                                value={this.state.startDate}
                                onChange={this.handleDateChange}
                                className="date-box"
                                InputLabelProps={{
                                    shrink: true,
                                }}
                                inputProps={{"data-testid": `sdate-input`}}
                            />
                            <TextField
                                
                                id="edate"
                                label="End Date"
                                type="datetime-local"
                                value={this.state.endDate}
                                onChange={this.handleDateChange}
                                className="date-box"
                                InputLabelProps={{
                                    shrink: true,
                                }}
                                inputProps={{"data-testid": `edate-input`}}
                            />
                            </Grid>
                        </div>
                        {/* submit button div, using material UI button and handling the event with a handleSubmit function */}
                        <div className="submit-button">
                            <Button data-testid="sub-button" id="button-sub" variant="outlined" color="secondary" onClick={this.handleSubmit} > Submit</Button>
                        </div>
                    </form>
                </div>
            </div>
        )
    }
}

export default Home
