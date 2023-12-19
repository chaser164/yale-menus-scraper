import { ClipLoader } from 'react-spinners';

export const Loader = (props) => {
  return (
    <div className="loader-container">
        <ClipLoader color="#3498db" loading={true} size={props.size} />
    </div>
  );
};
