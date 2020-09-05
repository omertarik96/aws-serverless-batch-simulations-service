import React, { useState, useEffect } from "react";
import Amplify, { Storage } from "aws-amplify";
import { AmplifyAuthenticator, AmplifySignOut } from "@aws-amplify/ui-react";
import { ThemeProvider, CSSReset, Spinner, Text } from "@chakra-ui/core";
import customTheme from "./theme";
import Header from "./Header";
import { AuthState, onAuthUIStateChange } from "@aws-amplify/ui-components";

Amplify.configure({
  Auth: {
    identityPoolId: "us-east-1:232d5933-cca5-48b7-ac39-f2e91e1c303c", //REQUIRED - Amazon Cognito Identity Pool ID
    region: "us-east-1", // REQUIRED - Amazon Cognito Region
    userPoolId: "us-east-1_EIoOQNk4H", //OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: "phvcq0d2f740g3ab4r7p76dag", //OPTIONAL - Amazon Cognito Web Client ID
  },
  Storage: {
    AWSS3: {
      bucket: "simulations-service-inputs3bucketec778848-1m5gdr91i4ebr", //REQUIRED -  Amazon S3 bucket name
      region: "us-east-1", //OPTIONAL -  Amazon service region
    },
  },
});

const App = () => {
  const [loading, setLoading] = useState(null);

  const [authState, setAuthState] = useState();
  const [user, setUser] = React.useState();

  useEffect(() => {
    return onAuthUIStateChange((nextAuthState, authData) => {
      setAuthState(nextAuthState);
      setUser(authData);
    });
  }, []);

  const onChange = (e) => {
    const file = e.target.files[0];
    setLoading(true);

    Storage.put(file.name, file, {
      contentType: "image/png",
    })
      .then((result) => {
        console.log(result);
        setLoading(false);
      })
      .catch((err) => console.log(err));
  };

  return (
    <ThemeProvider theme={customTheme}>
      <CSSReset />
      {authState === AuthState.SignedIn && user ? (
        <>
          <Header />
          <div className="flex w-full h-screen items-center justify-center bg-grey-lighter">
            {loading === null && (
              <label className="w-64 flex flex-col items-center px-4 py-6 bg-white text-blue-500 rounded-lg shadow-lg tracking-wide uppercase border border-blue-500 cursor-pointer hover:bg-blue-500 hover:text-white">
                <svg
                  className="w-8 h-8"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                >
                  <path d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z" />
                </svg>
                <span className="mt-2 text-base leading-normal">
                  Select a image file
                </span>
                <input type="file" className="hidden" onChange={onChange} />
              </label>
            )}
            {loading === true && (
              <>
                <Text>Uploading to S3.</Text>
                <Spinner color="blue" />
              </>
            )}
            {loading === false && (
              <Text>
                Your 10 simulations started simultaneously. Please check AWS
                console for details.
              </Text>
            )}
          </div>
        </>
      ) : (
        <div className="flex w-full h-screen items-center justify-center bg-grey-lighter">
          <AmplifyAuthenticator />
        </div>
      )}
    </ThemeProvider>
  );
};

export default App;
