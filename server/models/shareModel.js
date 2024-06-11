import mongoose from "mongoose";

const Schema = mongoose.Schema;

const shareSchema = new Schema({
  permissions: {
    type: String,
    required: true,
  },
});

const Share = mongoose.model("Share", shareSchema);
export default Share;
