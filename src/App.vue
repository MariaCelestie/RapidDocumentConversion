<template>
  <div>
    <h2 style="margin-bottom: 50px">PDF Converter</h2>
    <input
      id="file-input"
      type="file"
      @change="uploadFile"
      ref="file"
      accept=".doc, .docx"
      hidden
    />
    <label id="visual-button" for="file-input">Choose File</label>
    <label id="file-name">{{ fileName }}</label>
    <LoadingAnimation v-if="isConverting" />
    <button
      id="convert-btn"
      v-show="fileSelected && !isConverting"
      @click="submitFile"
    >
      CONVERT
    </button>
  </div>
</template>

<script>
import LoadingAnimation from "./components/LoadingAnimation";
export default {
  name: "App",
  components: {
    LoadingAnimation,
  },
  data() {
    return {
      fileSelected: false,
      fileName: "No File chosen!",
      isConverting: false,
    };
  },
  methods: {
    uploadFile() {
      this.file = this.$refs.file.files[0];
      this.fileSelected = true;
      this.fileName = this.file.name;
      console.log("File selected");
      console.log(this.file.name);
    },
    async submitFile() {
      this.isConverting = true;

      const formData = new FormData();
      formData.append("file", this.file);

      console.log(this.file);
      const headers = { "Content-Type": "multipart/form-data" };

      const res = await this.$axios.post(
        "http://127.0.0.1:5005/upload",
        formData,
        {
          headers,
        }
      );

      console.log(res);

      setTimeout(() => {
        console.log("converting");
        const link = document.createElement("a");

        //TESTING
        //Change type after pdf. it is just an example
        // const blob = new Blob([this.file], {
        //   type: " application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        // });
        // link.href = URL.createObjectURL(blob);

        //REAL ONE
        link.href =
          "https://converteddocument.s3.us-east-2.amazonaws.com/" +
          res.data +
          ".pdf";
        link.download = "download";
        link.click();
        URL.revokeObjectURL(link.href);
        this.isConverting = false;
      }, 2000);
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

#visual-button {
  background-color: #118ab2;
  color: white;
  padding: 0.5rem;
  font-family: sans-serif;
  border-radius: 0.5rem;
  cursor: pointer;
  margin-top: 150px;
}

#file-name {
  display: block;
  margin-top: 50px;
}

#convert-btn {
  margin-top: 50px;
  background-color: #d62828;
  color: white;
  font-family: sans-serif;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  width: 50%;
  height: 50px;
  font-size: 1.2rem;
  font-weight: bold;
}
</style>
