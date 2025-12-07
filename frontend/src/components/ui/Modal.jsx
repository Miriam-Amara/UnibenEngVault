/**
 * 
 */



export function ModalOverlay({
  children,
  className
}) {
  return (
    <div
      className={ `h-100 w-100 bg-grey-dark-75 absolute top-0 left-0 flex justify-center items-center ${className}` }
    >
      <div
        className="w-25 h-50 p-5 rounded-10 bg-white flex flex-col items-center gap-5"
      >
        { children }
      </div>
    </div>
  );
}


export function PopUp({
  children,
  className
}) {
  return (
    <div
      className={ `${innerStyles.base} ${innerStyles.position} ${innerStyles.flex} ${className}` }
    >
      { children }
    </div>
  );
}

const innerStyles = {
  base: "p-5 rounded-10 bg-white shadow-grey-md",
  position: "absolute top-50 left-50 translate",
  flex: "flex flex-col gap-2"
}