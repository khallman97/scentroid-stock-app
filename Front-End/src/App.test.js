import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";

import App from './App';

configure({ adapter: new Adapter() });


describe("App component" , () => {
  /* Test the application can render without crashing */
  test("renders without crashing", () => {
    shallow(<App />);
  });
})

