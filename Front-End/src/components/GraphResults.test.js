import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import GraphResults from './GraphResults'

configure({ adapter: new Adapter() });

describe("GraphResult Component" , () => {
      /* 
        Check the message with no data is there on data load 
        done using the default x and y range, that would be in
        the state upon load
      */
      test("enter data message on load" , () => {
        const wrapper = shallow(<GraphResults  xrange="" yrange="" />);
        const message = <h1>Please Enter a Range and Time Zone</h1>;
        expect(wrapper.contains(message)).toEqual(true);
      });

    })