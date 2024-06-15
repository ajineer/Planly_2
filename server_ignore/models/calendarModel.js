import mongoose from "mongoose";

const Schema = mongoose.Schema;

const calendarSchema = new Schema({
  name: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
});

const Calendar = mongoose.model("Calendar", calendarSchema);
export default Calendar;
