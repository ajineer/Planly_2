import mongoose from "mongoose";

const Schema = mongoose.Schema;

const eventSchema = new Schema({
  name: {
    type: String,
    required: true,
  },
  start: {
    type: String,
    required: true,
  },
  end: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: false,
  },
});

const Event = mongoose.model("Event", eventSchema);
export default Event;
