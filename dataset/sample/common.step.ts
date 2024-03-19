import { defineParameterType } from '@cucumber/cucumber'
import { expect } from '@playwright/test'

import { Given, Then, When } from '../common/fixtures'
import { getDataByKey, shortenAddress } from '../common/utils'

defineParameterType({
  name: 'listOfString',
  regexp: /\[([^\]]*)\]/,
  transformer: (str: string) => str.split(',').map((item) => item.trim()),
})

Given('I go to home page', async ({ basePage }) => {
  await basePage.goto()
})

Given('I go to login page', async ({ loginPage }) => {
  await loginPage.goto()
})

Given('I go to address page', async ({ addressPage }) => {
  await addressPage.goto()
})

When('I wait for {int} seconds', async ({ basePage }, seconds) => {
  await basePage.waitForTimeout(seconds * 1000)
})

When(
  'I type data with key {string} to input with role {string}',
  async ({ commonDataProvider, basePage }, dataKey, inputName) => {
    const dataContent = getDataByKey(commonDataProvider.commonData, dataKey)
    await basePage.fillByRoleTextbox(inputName, dataContent)
  },
)

When(
  'I type secret data with key {string} to input with locator {string}',
  async ({ secretDataProvider, basePage }, dataKey, inputName) => {
    const dataContent = getDataByKey(secretDataProvider.secretsData ?? dataKey, dataKey) ?? dataKey
    await basePage.fillByLocator(inputName, dataContent)
  },
)

When(
  'I type data with key {string} to input with locator {string}',
  async ({ commonDataProvider, basePage }, dataKey, inputName) => {
    const dataContent = getDataByKey(commonDataProvider.commonData, dataKey) ?? dataKey
    await basePage.fillByLocator(inputName, dataContent)
  },
)

When(
  'I type data with key {string} to input with placeholder {string}',
  async ({ commonDataProvider, basePage }, dataKey, placeholder) => {
    const dataContent = getDataByKey(commonDataProvider.commonData, dataKey) ?? dataKey
    await basePage.fillByPlaceholder(placeholder, dataContent)
  },
)

When('I type {string} to input with locator {string}', async ({ basePage }, dataContent, inputName) => {
  await basePage.fillByLocator(inputName, dataContent)
})

When('I type {string} to input with role {string}', async ({ basePage }, text, inputName) => {
  await basePage.fillByRoleTextbox(inputName, text)
})

When('I type {string} to input with placeholder {string}', async ({ basePage }, text, placeholder) => {
  await basePage.fillByPlaceholder(placeholder, text)
})

When(
  'I type {string} to input with placeholder {string} at index {int}',
  async ({ basePage }, text, placeholder, index) => {
    await basePage.getPage().getByPlaceholder(placeholder, { exact: true }).nth(index).fill(text)
  },
)

When(
  'I fill all the inputs with placeholder {string} with values: {listOfString}',
  async ({ basePage }, placeholder, values) => {
    for (let index = 0; index < values.length; index++) {
      const value = values[index]
      await basePage.getPage().getByPlaceholder(placeholder, { exact: true }).nth(index).fill(value)
    }
  },
)

When('I click element with label {string}', async ({ basePage }, label) => {
  await basePage.clickByLabel(label)
})

When('I click element with role {string} and name {string}', async ({ basePage }, role, name) => {
  await basePage.clickByRole(role, name)
})

When('I click element with text {string}', async ({ basePage }, text) => {
  await basePage.clickByText(text)
})

When('I click link {string}', async ({ basePage }, name) => {
  await basePage.clickByRole('link', name)
})

When('I click button {string}', async ({ basePage }, name) => {
  await basePage.clickByRole('button', name)
})

When('I click button {string} at index {int}', async ({ basePage }, name, index) => {
  await basePage.clickByRole('button', name, index)
})

When('I click button with locator {string}', async ({ basePage }, locator) => {
  await basePage.clickByLocator(locator)
})

When('I click button with locator {string} at index {int}', async ({ basePage }, locator, index) => {
  await basePage.clickByLocator(locator, index)
})

Then('I should be in home page', async ({ basePage }) => {
  await expect(basePage.getPage()).toHaveURL(basePage.getUrl())
})

Then('I expect that the title contains {string}', async ({ basePage }, keyword) => {
  await expect(basePage.getPage()).toHaveTitle(new RegExp(keyword))
})

Then('I expect that the text {string} is visible', async ({ basePage }, text) => {
  await expect(basePage.getPage().getByText(text, { exact: true }).first()).toBeVisible()
})

Then('I expect that the text {string} is invisible', async ({ basePage }, text) => {
  await expect(basePage.getPage().getByText(text, { exact: true }).first()).toBeHidden()
})

Then(
  'I expect that the text of data with key {string} is visible',
  async ({ commonDataProvider, basePage }, dataKey) => {
    const dataContent = getDataByKey(commonDataProvider.commonData, dataKey) ?? dataKey
    await expect(basePage.getPage().getByText(dataContent, { exact: true }).first()).toBeVisible()
  },
)

Then(
  'I expect that the text of data with key {string} is invisible',
  async ({ commonDataProvider, basePage }, dataKey) => {
    const dataContent = getDataByKey(commonDataProvider.commonData, dataKey) ?? dataKey
    await expect(basePage.getPage().getByText(dataContent, { exact: true }).first()).toBeHidden()
  },
)

Then('I expect that element with locator {string} is invisible', async ({ basePage }, locator) => {
  await expect(basePage.getPage().locator(locator).first()).toBeHidden()
})

Then('I expect that element with locator {string} is visible', async ({ basePage }, locator) => {
  await expect(basePage.getPage().locator(locator).first()).toBeVisible()
})

Then('I expect that button with text {string} is visible', async ({ basePage }, text) => {
  await expect(basePage.getPage().getByRole('button', { name: text, exact: true }).first()).toBeVisible()
})

Then('I expect that the element with text {string} is invisible', async ({ basePage }, text) => {
  // order is 0-based
  await expect(basePage.getPage().getByText(text, { exact: true })).toBeHidden()
})

Then('I expect that the element with role {string} and order {int} is visible', async ({ basePage }, text, order) => {
  // order is 0-based
  await expect(basePage.getPage().getByRole(text, { exact: true }).nth(order)).toBeVisible()
})

Then('I expect that I go back to the {string} page', async ({ basePage }, pageName) => {
  // Check if whether we are on vaults page
  await expect(
    basePage.getPage().getByRole('heading', {
      name: pageName,
    }),
  ).toBeVisible()
})

Then('I expect that the address {string} is visible', async ({ commonDataProvider, basePage }, dataKey) => {
  const addressStr = shortenAddress(getDataByKey(commonDataProvider.commonData, dataKey))
  await expect(basePage.getPage().getByText(addressStr)).toBeVisible()
})

Then(
  'I expect that the address {string} with order {int} is invisible',
  async ({ commonDataProvider, basePage }, dataKey, order) => {
    const addressStr = shortenAddress(getDataByKey(commonDataProvider.commonData, dataKey))
    await expect(basePage.getPage().getByText(addressStr).nth(order)).toBeVisible()
  },
)

Then(
  'I expect that row number {int} in table contains these values: {listOfString}',
  async ({ basePage }, index, values) => {
    await basePage.getPage().waitForSelector('table') // wait to load data table
    // 1-based index
    const firstRow = await basePage.getPage().locator('table tr').nth(index)
    for (const value of values) {
      await expect(firstRow).toContainText(value)
    }
  },
)

Then('I expect that the table contains {int} record', async ({ basePage }, total) => {
  await basePage.getPage().waitForSelector('table') // wait for the data table to load
  const size = await basePage.getPage().locator('table tr').count()
  expect(size).toBe(total + 1)
})