import React, { Component } from 'react'

//Line chart from Chart.js and react-chartjs-2 wrapper
import { Line } from 'react-chartjs-2';

//CSS file for components
import './ComponentStyles.css'

export class GraphResults extends Component {
    
    render() {
        /* 
            Data format for the Line Chart, uses the data that is in the props and passed
            from the parent class
        */
        const data = {
            labels: this.props.xrange,
            datasets: [
                {
                label: 'Stock Price',
                data: this.props.yrange,
                fill: false,
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgba(0, 0, 0, 0.2)',
                borderWidth: 1,
                tension: 0.1
                },
            ],
        };
        //Options format for the Line Chart    
        const options = {
            scales: {
                yAxes: [
                  {
                    ticks: {
                      beginAtZero: false,
                    },
                  },
                ],
              },
        };
        /*
            If the data from the props is empty (api request not made) return the text on the screen 
            Else return a div with the Line Graph inside of it
        */
        if(this.props.xrange == "" ) {
            return(
                <div>
                    <h1>Please Enter a Range and Time Zone</h1>
                </div>
            ) 
        } else {
            return (
                <div className="graph-holder" data-testid="graph-div">
                    <Line data={data} options={options} />
                </div>
            ) 
        }
        
    }
}

export default GraphResults
