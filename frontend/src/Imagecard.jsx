import React from "react";

const ImageCard = ({ image }) => {
  return (
    <div style={{
      border: "1px solid #ddd",
      borderRadius: "8px",
      padding: "10px",
      margin: "10px",
      width: "200px",
      textAlign: "center"
    }}>
      <img 
        src={`http://127.0.0.1:8000/images/${image.filename}`} 
        alt={image.filename} 
        style={{ width: "100%", height: "150px", objectFit: "cover", borderRadius: "5px" }} 
      />
      <p>{image.filename}</p>
    </div>
  );
};

export default ImageCard;
