import React from "react";
import { Box, Heading, Flex, Text } from "@chakra-ui/core";
import { AmplifySignOut } from "@aws-amplify/ui-react";

const MenuItems = ({ children }) => (
  <Text mt={{ base: 4, md: 0 }} mr={6} display="block">
    {children}
  </Text>
);

const Header = (props) => {
  const [show, setShow] = React.useState(false);
  const handleToggle = () => setShow(!show);

  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="1.5rem"
      className="bg-blue-500"
      color="white"
      {...props}
    >
      <Flex align="center" mr={5}>
        <Heading as="h1" size="lg">
          Simulations Service
        </Heading>
      </Flex>

      <Box display={{ sm: "block", md: "none" }} onClick={handleToggle}>
        <svg
          fill="white"
          width="12px"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <title>Menu</title>
          <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
        </svg>
      </Box>

      <Box
        display={{ sm: show ? "block" : "none", md: "flex" }}
        width={{ sm: "full", md: "auto" }}
        alignItems="center"
        flexGrow={1}
      >
        <MenuItems>
          <a
            target="_blank"
            className="text-reset"
            href="https://s3.console.aws.amazon.com/s3/buckets/simulations-service-inputs3bucketec778848-1m5gdr91i4ebr/?region=us-east-1&tab=overview"
          >
            AWS S3
          </a>
        </MenuItems>
        <MenuItems>
          <a
            target="_blank"
            className="text-reset"
            href="https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=simulations-service-JobTable0F869D99-1HZBMUKUO4PX;tab=items"
          >
            AWS DynamoDB
          </a>
        </MenuItems>
        <MenuItems>
          <a
            target="_blank"
            className="text-reset"
            href="https://console.aws.amazon.com/batch/home?region=us-east-1#/jobs/queue/arn:aws:batch:us-east-1:837128449882:job-queue~2FJobQueueEE3AD499-c8e639339fe06eb/job/a586bf75-8eb9-4093-b3e2-9cd03bb5e175?state=SUCCEEDED"
          >
            AWS Batch
          </a>
        </MenuItems>
      </Box>

      <Box
        display={{ sm: show ? "block" : "none", md: "block" }}
        mt={{ base: 4, md: 0 }}
      >
        <AmplifySignOut />
        {/* <Button bg="transparent" border="1px">
          Sign Out
        </Button> */}
      </Box>
    </Flex>
  );
};

export default Header;
